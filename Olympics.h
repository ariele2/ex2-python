#ifndef OLYMPICS_H
#define OLYMPICS_H

#include<stdio.h>
#include<string.h>
#include<stdbool.h>
#include<stdlib.h>

typedef struct olympics* Olympics;

Olympics OlympicsCreate();

void OlympicsUpdateCompetitionResults(Olympics o, const char* gold_country, const char* silver_country, const char* bronze_country);

void OlympicsWinningCountry(Olympics o);

void OlympicsDestroy(Olympics o);

#endif