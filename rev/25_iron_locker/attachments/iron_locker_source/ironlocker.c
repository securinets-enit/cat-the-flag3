#include <jni.h>
#include <stdint.h>
#include <string.h>

typedef struct {
    uint8_t bytes[96];
    uint32_t length;
    uint8_t live;
} Slot;

static Slot slot;

static const uint8_t recovery[] = {
    14, 241, 168, 119, 75, 25, 201, 187, 97, 63, 198, 244,
    184, 124, 36, 252, 163, 109, 100, 26, 200, 142, 115, 34,
    224, 207, 172, 68, 4, 253, 171, 89, 81, 29, 205, 135,
    109, 57, 234, 219, 134, 81
};

JNIEXPORT jlong JNICALL
Java_enit_ironlocker_LockerBridge_nativeCreate(JNIEnv *env, jclass cls,
                                                jbyteArray input) {
    (void) cls;
    jsize size = (*env)->GetArrayLength(env, input);
    if (size > (jsize) sizeof(slot.bytes)) size = sizeof(slot.bytes);
    memset(&slot, 0, sizeof(slot));
    (*env)->GetByteArrayRegion(env, input, 0, size, (jbyte *) slot.bytes);
    slot.length = (uint32_t) size;
    slot.live = 1;
    if (size != 32) {
        slot.length = 8 + sizeof(recovery);
        memcpy(slot.bytes, "ILKR", 4);
        slot.bytes[4] = 1;
        slot.bytes[5] = 7;
        slot.bytes[6] = sizeof(recovery) & 0xff;
        slot.bytes[7] = sizeof(recovery) >> 8;
        memcpy(slot.bytes + 8, recovery, sizeof(recovery));
    }
    return (jlong) (uintptr_t) &slot;
}

JNIEXPORT void JNICALL
Java_enit_ironlocker_LockerBridge_nativeRemove(JNIEnv *env, jclass cls,
                                               jlong handle) {
    (void) env; (void) cls; (void) handle;
    slot.live = 0;
}

JNIEXPORT jbyteArray JNICALL
Java_enit_ironlocker_LockerBridge_nativeRead(JNIEnv *env, jclass cls,
                                             jlong handle) {
    (void) cls;
    Slot *stale = (Slot *) (uintptr_t) handle;
    jbyteArray out = (*env)->NewByteArray((jsize) stale->length);
    (*env)->SetByteArrayRegion(env, out, 0, (jsize) stale->length,
                               (jbyte *) stale->bytes);
    return out;
}
