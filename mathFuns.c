#include <math.h>

double calculateMean(double data[], int size) {
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        sum += data[i];
    }
    return sum / size;
}

double calculateSD(double data[], int size) {
    double mean = calculateMean(data, size), SD = 0.0;
    for (int i = 0; i < size; ++i) {
        SD += pow(data[i] - mean, 2);
    }
    return sqrt(SD / size);
}