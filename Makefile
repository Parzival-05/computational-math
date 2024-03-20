main: main.c
	gcc main.c mathFuns.c -o main -O3 -fopenmp -lm