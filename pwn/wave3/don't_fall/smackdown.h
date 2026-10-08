#ifndef SMACKDOWN_H
#define SMACKDOWN_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <stdbool.h>

/*
 *  WWE SMACKDOWN: RING OF CHAOS
 *  Championship Title Match CTF Challenge
 */

typedef struct {
    char *arena[20];            /* Pointers to arena row buffers (heap)     */
    char wrestler_tag[8];       /* Player's wrestler tag (user-controlled)  */
    int title_match_ready;      /* Must be non-zero to unlock title match   */
} ring_t;

static const char *banner =
"\n"
"    ██╗    ██╗██╗    ██╗███████╗\n"
"    ██║    ██║██║    ██║██╔════╝\n"
"    ██║ █╗ ██║██║ █╗ ██║█████╗  \n"
"    ██║███╗██║██║███╗██║██╔══╝  \n"
"    ╚███╔███╔╝╚███╔███╔╝███████╗\n"
"     ╚══╝╚══╝  ╚══╝╚══╝ ╚══════╝\n"
"\n"
"    ============================================\n"
"      SMACKDOWN : RING OF CHAOS\n"
"      [  Championship Title Match  ]\n"
"    ============================================\n";

static const char *commentary[] = {
    "BAH GAWD! WHAT A MANEUVER!",
    "HE'S BROKEN IN HALF!",
    "AS GOD AS MY WITNESS!",
    "THAT MAN HAS A FAMILY!",
    "STONE COLD! STONE COLD! STONE COLD!",
    "THE MOST ELECTRIFYING MOVE IN SPORTS ENTERTAINMENT!",
    "CAN YOU SMELL WHAT THE ROCK IS COOKING?!",
    "VINTAGE SMACKDOWN!",
    "THIS IS EXTREME!",
    "WHAT A SLOBBERKNOCKER!",
    "OH MY! OH MY! OH MY!",
    "IT'S A SLOBBERKNOCKER, KING!",
};

#define NUM_COMMENTARY 12

#endif /* SMACKDOWN_H */
