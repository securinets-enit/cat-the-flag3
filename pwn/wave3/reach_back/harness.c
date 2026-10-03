#define _GNU_SOURCE

#include <dlfcn.h>
#include <elf.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>

#define MAX_SO_SIZE (256U * 1024U)

#ifndef STT_GNU_IFUNC
#define STT_GNU_IFUNC 10
#endif

typedef void (*solve_fn)(void);

extern int caller(solve_fn solve);

static int write_all(int fd, const char *buffer, size_t length) {
    while (length != 0U) {
        ssize_t written = write(fd, buffer, length);

        if (written < 0 && errno == EINTR) {
            continue;
        }
        if (written <= 0) {
            return -1;
        }
        buffer += (size_t)written;
        length -= (size_t)written;
    }
    return 0;
}

#define SAY(fd, text) ((void)write_all((fd), (text), sizeof(text) - 1U))

static int region_is_valid(uint64_t offset, uint64_t count,
                           uint64_t item_size, size_t file_size) {
    uint64_t bytes;

    if (item_size != 0U && count > UINT64_MAX / item_size) {
        return 0;
    }
    bytes = count * item_size;
    if (offset > (uint64_t)file_size) {
        return 0;
    }
    return bytes <= (uint64_t)file_size - offset;
}

static int vaddr_to_offset(const Elf64_Phdr *program_headers,
                           size_t program_header_count, uint64_t address,
                           uint64_t length, size_t file_size,
                           uint64_t *result) {
    size_t index;

    for (index = 0; index < program_header_count; index++) {
        const Elf64_Phdr *header = &program_headers[index];
        uint64_t delta;

        if (header->p_type != PT_LOAD || address < header->p_vaddr) {
            continue;
        }
        delta = address - header->p_vaddr;
        if (delta > header->p_filesz || length > header->p_filesz - delta) {
            continue;
        }
        if (header->p_offset > UINT64_MAX - delta) {
            continue;
        }
        *result = header->p_offset + delta;
        return region_is_valid(*result, length, 1U, file_size);
    }
    return 0;
}

static int relocation_table_is_safe(const unsigned char *mapping,
                                    size_t file_size,
                                    const Elf64_Phdr *program_headers,
                                    size_t program_header_count,
                                    uint64_t address, uint64_t byte_count,
                                    uint64_t entry_size, int is_rela) {
    uint64_t offset;
    uint64_t index;
    uint64_t count;
    uint64_t expected_size = is_rela ? sizeof(Elf64_Rela) : sizeof(Elf64_Rel);

    if (byte_count == 0U) {
        return 1;
    }
    if (address == 0U || entry_size != expected_size ||
        byte_count % entry_size != 0U ||
        !vaddr_to_offset(program_headers, program_header_count, address,
                         byte_count, file_size, &offset)) {
        return 0;
    }

    count = byte_count / entry_size;
    for (index = 0; index < count; index++) {
        uint64_t info;

        if (is_rela) {
            const Elf64_Rela *relocation =
                (const Elf64_Rela *)(mapping + offset + index * entry_size);
            info = relocation->r_info;
        } else {
            const Elf64_Rel *relocation =
                (const Elf64_Rel *)(mapping + offset + index * entry_size);
            info = relocation->r_info;
        }
        if (ELF64_R_TYPE(info) == R_X86_64_IRELATIVE) {
            return 0;
        }
    }
    return 1;
}

struct dynamic_info {
    uint64_t symtab;
    uint64_t syment;
    uint64_t rela;
    uint64_t relasz;
    uint64_t relaent;
    uint64_t rel;
    uint64_t relsz;
    uint64_t relent;
    uint64_t jmprel;
    uint64_t pltrelsz;
    uint64_t pltrel;
};

static int inspect_dynamic_table(const unsigned char *mapping, size_t file_size,
                                 const Elf64_Phdr *header,
                                 struct dynamic_info *information,
                                 char *reason, size_t reason_size) {
    const Elf64_Dyn *entries;
    size_t count;
    size_t index;
    int saw_null = 0;

    if (header->p_filesz == 0U ||
        header->p_filesz % sizeof(Elf64_Dyn) != 0U ||
        !region_is_valid(header->p_offset, header->p_filesz, 1U, file_size)) {
        snprintf(reason, reason_size, "invalid PT_DYNAMIC table");
        return 0;
    }

    entries = (const Elf64_Dyn *)(mapping + header->p_offset);
    count = (size_t)(header->p_filesz / sizeof(Elf64_Dyn));
    for (index = 0; index < count; index++) {
        const Elf64_Dyn *entry = &entries[index];

        if (entry->d_tag == DT_NULL) {
            saw_null = 1;
            break;
        }
        switch (entry->d_tag) {
        case DT_INIT:
        case DT_INIT_ARRAY:
        case DT_PREINIT_ARRAY:
        case DT_NEEDED:
            snprintf(reason, reason_size,
                     "constructors and extra dependencies are not allowed");
            return 0;
#ifdef DT_AUXILIARY
        case DT_AUXILIARY:
#endif
#ifdef DT_FILTER
        case DT_FILTER:
#endif
            snprintf(reason, reason_size, "dynamic loader filters are not allowed");
            return 0;
        case DT_SYMTAB:
            information->symtab = entry->d_un.d_ptr;
            break;
        case DT_SYMENT:
            information->syment = entry->d_un.d_val;
            break;
        case DT_RELA:
            information->rela = entry->d_un.d_ptr;
            break;
        case DT_RELASZ:
            information->relasz = entry->d_un.d_val;
            break;
        case DT_RELAENT:
            information->relaent = entry->d_un.d_val;
            break;
        case DT_REL:
            information->rel = entry->d_un.d_ptr;
            break;
        case DT_RELSZ:
            information->relsz = entry->d_un.d_val;
            break;
        case DT_RELENT:
            information->relent = entry->d_un.d_val;
            break;
        case DT_JMPREL:
            information->jmprel = entry->d_un.d_ptr;
            break;
        case DT_PLTRELSZ:
            information->pltrelsz = entry->d_un.d_val;
            break;
        case DT_PLTREL:
            information->pltrel = entry->d_un.d_val;
            break;
        default:
            break;
        }
    }

    if (!saw_null) {
        snprintf(reason, reason_size, "unterminated PT_DYNAMIC table");
        return 0;
    }
    return 1;
}

static int validate_symbols(const unsigned char *mapping, size_t file_size,
                            const Elf64_Ehdr *elf_header,
                            const Elf64_Shdr *section_headers,
                            const struct dynamic_info *dynamic,
                            char *reason, size_t reason_size) {
    size_t section_index;
    int found_dynamic_symbols = 0;
    int found_solve = 0;

    for (section_index = 0; section_index < elf_header->e_shnum;
         section_index++) {
        const Elf64_Shdr *section = &section_headers[section_index];
        const Elf64_Shdr *string_section;
        const Elf64_Sym *symbols;
        const char *strings;
        size_t symbol_count;
        size_t symbol_index;

        if (section->sh_type == SHT_NOBITS) {
            continue;
        }
        if (!region_is_valid(section->sh_offset, section->sh_size, 1U,
                             file_size)) {
            snprintf(reason, reason_size, "section extends beyond the file");
            return 0;
        }
        if ((section->sh_type == SHT_INIT_ARRAY ||
             section->sh_type == SHT_PREINIT_ARRAY) &&
            section->sh_size != 0U) {
            snprintf(reason, reason_size, "initializer arrays are not allowed");
            return 0;
        }
        if (section->sh_type != SHT_DYNSYM && section->sh_type != SHT_SYMTAB) {
            continue;
        }
        if (section->sh_entsize != sizeof(Elf64_Sym) ||
            section->sh_size % sizeof(Elf64_Sym) != 0U ||
            section->sh_link >= elf_header->e_shnum) {
            snprintf(reason, reason_size, "invalid symbol table");
            return 0;
        }

        string_section = &section_headers[section->sh_link];
        if (string_section->sh_type != SHT_STRTAB ||
            !region_is_valid(string_section->sh_offset,
                             string_section->sh_size, 1U, file_size)) {
            snprintf(reason, reason_size, "invalid symbol string table");
            return 0;
        }

        if (section->sh_type == SHT_DYNSYM) {
            found_dynamic_symbols = 1;
            if (section->sh_addr != dynamic->symtab ||
                dynamic->syment != sizeof(Elf64_Sym)) {
                snprintf(reason, reason_size,
                         "dynamic symbol metadata does not match");
                return 0;
            }
        }

        symbols = (const Elf64_Sym *)(mapping + section->sh_offset);
        strings = (const char *)(mapping + string_section->sh_offset);
        symbol_count = (size_t)(section->sh_size / sizeof(Elf64_Sym));
        for (symbol_index = 0; symbol_index < symbol_count; symbol_index++) {
            const Elf64_Sym *symbol = &symbols[symbol_index];
            const char *name;
            size_t remaining;
            unsigned int type = ELF64_ST_TYPE(symbol->st_info);
            unsigned int binding = ELF64_ST_BIND(symbol->st_info);

            if (type == STT_GNU_IFUNC) {
                snprintf(reason, reason_size, "GNU IFUNC symbols are not allowed");
                return 0;
            }
            if (symbol->st_name >= string_section->sh_size) {
                snprintf(reason, reason_size, "symbol name is out of bounds");
                return 0;
            }
            name = strings + symbol->st_name;
            remaining = (size_t)(string_section->sh_size - symbol->st_name);
            if (memchr(name, '\0', remaining) == NULL) {
                snprintf(reason, reason_size, "unterminated symbol name");
                return 0;
            }
            if (section->sh_type == SHT_DYNSYM && strcmp(name, "solve") == 0 &&
                symbol->st_shndx != SHN_UNDEF) {
                if (type != STT_FUNC ||
                    (binding != STB_GLOBAL && binding != STB_WEAK)) {
                    snprintf(reason, reason_size,
                             "solve must be an exported function");
                    return 0;
                }
                found_solve = 1;
            }
        }
    }

    if (!found_dynamic_symbols || !found_solve) {
        snprintf(reason, reason_size, "exported function solve was not found");
        return 0;
    }
    return 1;
}

static int validate_shared_object(const char *path, char *reason,
                                  size_t reason_size) {
    int descriptor = -1;
    struct stat status;
    unsigned char *mapping = MAP_FAILED;
    const Elf64_Ehdr *elf_header;
    const Elf64_Phdr *program_headers;
    const Elf64_Shdr *section_headers;
    struct dynamic_info dynamic = {0};
    size_t index;
    int dynamic_count = 0;
    int valid = 0;

    descriptor = open(path, O_RDONLY | O_CLOEXEC | O_NOFOLLOW);
    if (descriptor < 0) {
        snprintf(reason, reason_size, "cannot open upload: %s", strerror(errno));
        return 0;
    }
    if (fstat(descriptor, &status) != 0 || !S_ISREG(status.st_mode)) {
        snprintf(reason, reason_size, "upload is not a regular file");
        goto cleanup;
    }
    if (status.st_size <= 0 || (uint64_t)status.st_size > MAX_SO_SIZE) {
        snprintf(reason, reason_size, "upload size is outside the allowed range");
        goto cleanup;
    }

    mapping = mmap(NULL, (size_t)status.st_size, PROT_READ, MAP_PRIVATE,
                   descriptor, 0);
    if (mapping == MAP_FAILED) {
        snprintf(reason, reason_size, "cannot map upload: %s", strerror(errno));
        goto cleanup;
    }
    if ((size_t)status.st_size < sizeof(Elf64_Ehdr)) {
        snprintf(reason, reason_size, "file is too small to be an ELF object");
        goto cleanup;
    }

    elf_header = (const Elf64_Ehdr *)mapping;
    if (memcmp(elf_header->e_ident, ELFMAG, SELFMAG) != 0 ||
        elf_header->e_ident[EI_CLASS] != ELFCLASS64 ||
        elf_header->e_ident[EI_DATA] != ELFDATA2LSB ||
        elf_header->e_ident[EI_VERSION] != EV_CURRENT ||
        elf_header->e_type != ET_DYN || elf_header->e_machine != EM_X86_64 ||
        elf_header->e_version != EV_CURRENT ||
        elf_header->e_ehsize != sizeof(Elf64_Ehdr)) {
        snprintf(reason, reason_size, "expected an x86-64 ET_DYN ELF object");
        goto cleanup;
    }
    if (elf_header->e_phnum == 0U || elf_header->e_phnum == PN_XNUM ||
        elf_header->e_phentsize != sizeof(Elf64_Phdr) ||
        !region_is_valid(elf_header->e_phoff, elf_header->e_phnum,
                         sizeof(Elf64_Phdr), (size_t)status.st_size)) {
        snprintf(reason, reason_size, "invalid program header table");
        goto cleanup;
    }
    if (elf_header->e_shnum == 0U || elf_header->e_shstrndx == SHN_XINDEX ||
        elf_header->e_shentsize != sizeof(Elf64_Shdr) ||
        !region_is_valid(elf_header->e_shoff, elf_header->e_shnum,
                         sizeof(Elf64_Shdr), (size_t)status.st_size)) {
        snprintf(reason, reason_size, "a valid section table is required");
        goto cleanup;
    }

    program_headers =
        (const Elf64_Phdr *)(mapping + (size_t)elf_header->e_phoff);
    section_headers =
        (const Elf64_Shdr *)(mapping + (size_t)elf_header->e_shoff);

    for (index = 0; index < elf_header->e_phnum; index++) {
        const Elf64_Phdr *header = &program_headers[index];

        if (header->p_filesz > header->p_memsz ||
            !region_is_valid(header->p_offset, header->p_filesz, 1U,
                             (size_t)status.st_size)) {
            snprintf(reason, reason_size, "invalid loadable segment");
            goto cleanup;
        }
        if (header->p_type == PT_DYNAMIC) {
            dynamic_count++;
            if (dynamic_count > 1 ||
                !inspect_dynamic_table(mapping, (size_t)status.st_size, header,
                                       &dynamic, reason, reason_size)) {
                goto cleanup;
            }
        }
    }
    if (dynamic_count != 1) {
        snprintf(reason, reason_size, "exactly one PT_DYNAMIC segment is required");
        goto cleanup;
    }

    if (!relocation_table_is_safe(
            mapping, (size_t)status.st_size, program_headers,
            elf_header->e_phnum, dynamic.rela, dynamic.relasz,
            dynamic.relaent == 0U ? sizeof(Elf64_Rela) : dynamic.relaent, 1) ||
        !relocation_table_is_safe(
            mapping, (size_t)status.st_size, program_headers,
            elf_header->e_phnum, dynamic.rel, dynamic.relsz,
            dynamic.relent == 0U ? sizeof(Elf64_Rel) : dynamic.relent, 0)) {
        snprintf(reason, reason_size, "invalid or unsafe relocation table");
        goto cleanup;
    }
    if (dynamic.pltrelsz != 0U) {
        int is_rela = dynamic.pltrel == DT_RELA;
        uint64_t entry_size = is_rela ? sizeof(Elf64_Rela) : sizeof(Elf64_Rel);

        if ((dynamic.pltrel != DT_RELA && dynamic.pltrel != DT_REL) ||
            !relocation_table_is_safe(
                mapping, (size_t)status.st_size, program_headers,
                elf_header->e_phnum, dynamic.jmprel, dynamic.pltrelsz,
                entry_size, is_rela)) {
            snprintf(reason, reason_size, "invalid or unsafe PLT relocations");
            goto cleanup;
        }
    }
    if (!validate_symbols(mapping, (size_t)status.st_size, elf_header,
                          section_headers, &dynamic, reason, reason_size)) {
        goto cleanup;
    }

    valid = 1;

cleanup:
    if (mapping != MAP_FAILED) {
        (void)munmap(mapping, (size_t)status.st_size);
    }
    if (descriptor >= 0) {
        (void)close(descriptor);
    }
    return valid;
}

#define ALLOW_SYSCALL(number)                                                \
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, (number), 0, 1),                    \
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)

__attribute__((noinline, visibility("hidden"))) int install_seccomp(void) {
    static const struct sock_filter filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 (uint32_t)offsetof(struct seccomp_data, arch)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
                 (uint32_t)offsetof(struct seccomp_data, nr)),
        ALLOW_SYSCALL(__NR_write),
        ALLOW_SYSCALL(__NR_exit),
        ALLOW_SYSCALL(__NR_exit_group),
        ALLOW_SYSCALL(__NR_rt_sigreturn),
        BPF_STMT(BPF_RET | BPF_K,
                 SECCOMP_RET_ERRNO | (EPERM & SECCOMP_RET_DATA)),
    };
    const struct sock_fprog program = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = (struct sock_filter *)filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1L, 0L, 0L, 0L) != 0) {
        return -1;
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &program) != 0) {
        return -1;
    }
    return 0;
}

int main(int argc, char **argv) {
    char reason[192];
    void *handle;
    void *symbol;
    const char *loader_error;
    solve_fn solve;
    int result;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s ./solve.so\n", argv[0]);
        return 2;
    }

    SAY(STDOUT_FILENO, "[harness] validating shared object...\n");
    if (!validate_shared_object(argv[1], reason, sizeof(reason))) {
        fprintf(stderr, "[harness] rejected upload: %s\n", reason);
        return 1;
    }
    SAY(STDOUT_FILENO,
        "[harness] validation passed; loading solve...\n");

    handle = dlopen(argv[1], RTLD_NOW | RTLD_LOCAL);
    if (handle == NULL) {
        fprintf(stderr, "[harness] dlopen failed: %s\n", dlerror());
        return 1;
    }

    (void)dlerror();
    symbol = dlsym(handle, "solve");
    loader_error = dlerror();
    if (loader_error != NULL || symbol == NULL) {
        fprintf(stderr, "[harness] dlsym(solve) failed: %s\n",
                loader_error != NULL ? loader_error : "symbol is null");
        (void)dlclose(handle);
        return 1;
    }
    _Static_assert(sizeof(solve) == sizeof(symbol),
                   "function and data pointers must have equal size");
    memcpy(&solve, &symbol, sizeof(solve));

    SAY(STDOUT_FILENO,
        "[harness] solve resolved; preparing caller stack and sandbox...\n");
    result = caller(solve);

    if (result == 0) {
        SAY(STDOUT_FILENO, "\n[harness] solve returned cleanly.\n");
        _exit(0);
    }
    if (result == 1) {
        SAY(STDERR_FILENO, "[harness] could not read /flag (or local ./flag).\n");
    } else {
        SAY(STDERR_FILENO, "[harness] could not install seccomp.\n");
    }
    _exit(1);
}
