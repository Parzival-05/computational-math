#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <math.h>

#define MIN(a,b) (((a)<(b))?(a):(b))

const size_t BLOCK_SIZE = 64;
const double EPS = 0.0001;

typedef struct dirichlet_problem {
    size_t N;
    double h;
    double** f;
    double** u;
} dirichlet_problem;

double f1(double x, double y) {
    return 0;
}
double f2(double x, double y) {
    return pow(exp(x), y) * (x * x + y * y);
}

double g1(double x, double y) {
    double res = 0;
    if (x == 0) {
        res = 1 - 2 * y;
    }
    else if (x == 1) {
        res = -1 + 2 * y;
    }
    else if (y == 0) {
        res = 1 - 2 * x;
    }
    else if (y == 1) {
        res = -1 + 2 * x;
    }
    return 100 * res;
}

double g2(double x, double y) {
    double res = 0;
    if (x == 0) {
        res = 1;
    }
    else if (x == 1) {
        res = exp(-y);
    }
    else if (y == 0) {
        res = 1;
    }
    else if (y == 1) {
        res = exp(-x);
    }
    return res;
}

void free_dp(dirichlet_problem dp) {
    for (size_t i = 0; i < dp.N; i++) {
        free(dp.u[i]);
        free(dp.f[i]);
    }
    free(dp.u);
    free(dp.f);
}

double** create_grid_with_borders(size_t N) {
    size_t i, size_of_grid = N + 2;
    double** grid = calloc(size_of_grid, sizeof(double*));
    for (i = 0; i < size_of_grid; i++) {
        double* row = calloc(size_of_grid, sizeof(double));
        grid[i] = row;
    }
    return grid;
}

double proccess_block(dirichlet_problem* dp, size_t i_block, size_t j_block) {
    double d = 0, temp, h = dp->h;
    double** u = dp->u;
    double** f = dp->f;
    size_t i_upper_left = i_block * BLOCK_SIZE + 1;
    size_t j_upper_left = j_block * BLOCK_SIZE + 1;
    size_t i_lower_right = i_upper_left + MIN(BLOCK_SIZE, dp->N - i_upper_left + 1);
    size_t j_lower_right = j_upper_left + MIN(BLOCK_SIZE, dp->N - j_upper_left + 1);
    int i, j;
    double dm = 0;
    for (i = i_upper_left; i < i_lower_right; i++) {
        for (j = j_upper_left; j < j_lower_right; j++) {
            temp = u[i][j];
            dp->u[i][j] = 0.25 * (u[i - 1][j] + u[i + 1][j] + u[i][j - 1] + u[i][j + 1] - h * h * f[i][j]);
            d = fabs(temp - u[i][j]);
            if (dm < d) dm = d;
        }
    }
    return dm;
}

size_t approximate_dirichlet(dirichlet_problem* dp) {
    int k = 0, nx, NB;
    NB = dp->N / BLOCK_SIZE;
    NB += (dp->N % BLOCK_SIZE) == 0 ? 0 : 1;
    double dmax = 0, d = 0;
    double* dm = calloc(NB, sizeof(double));
    int i, j;
    do {
        k++;
        dmax = 0;
        for (nx = 0; nx < NB; nx++) {
            dm[nx] = 0;
#pragma omp parallel for shared(dp, nx, dm) private(i,j,d) 
            for (i = 0; i < nx + 1; i++) {
                j = nx - i;
                d = proccess_block(dp, i, j);
                if (dm[i] < d) dm[i] = d;
            }
        }
        for (nx = NB - 2; nx > -1; nx--) {
#pragma omp parallel for shared(dp, nx, dm) private(i,j,d) 
            for (i = NB - nx - 1; i < NB; i++) {
                j = 2 * (NB - 1) - nx - i;
                d = proccess_block(dp, i, j);
                if (dm[i] < d) dm[i] = d;
            }
        }
        for (int i = 0; i < NB; i++) {
            if (dmax < dm[i])
                dmax = dm[i];
        }
    } while (dmax > EPS);
    free(dm);
    return k;
}

dirichlet_problem init_dp(double (*f_fun)(double, double), double (*g_fun)(double, double), size_t N) {
    dirichlet_problem dp;
    double h = 1.0 / (N + 1);
    double** f = create_grid_with_borders(N);
    double** u = create_grid_with_borders(N);
    for (size_t i = 1; i < N + 1; i++) {
        for (size_t j = 1; j < N + 1; j++) {
            f[i][j] = f_fun(i * h, j * h);
        }
    }
    for (size_t index = 0; index < N + 2; index++) {
        u[0][index] = g_fun(0, index * h);
        u[N + 1][index] = g_fun(1, index * h);
        u[index][0] = g_fun(index * h, 0);
        u[index][N + 1] = g_fun(index * h, 1);
    }
    dp.u = u;
    dp.f = f;
    dp.h = h;
    dp.N = N;
    return dp;
}

int main()
{
    size_t s, k;
    dirichlet_problem dp;
    size_t grids[] = { 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000 };
    size_t threads[] = { 1, 2, 4, 8, 12 };
    size_t length_of_grids = sizeof(grids) / sizeof(size_t);
    size_t length_of_threads = sizeof(threads) / sizeof(size_t);
    double t, t1, t2, acceleration;
    printf("-------------------------------------------------------------------------------------------------------------------------\n");
    printf("|\tSize of grid\t|\tIterations\t|\tTime\t\t|\tAcceleration\t|\tThreads\t\t|\n");
    printf("-------------------------------------------------------------------------------------------------------------------------\n");
    for (int i = 0; i < length_of_grids; i++) {
        s = grids[i];
        for (int j = 0; j < length_of_threads; j++) {
            size_t thread = threads[j];
            dp = init_dp(&f2, &g2, s);
            omp_set_num_threads(thread);
            t1 = omp_get_wtime();
            k = approximate_dirichlet(&dp);
            t2 = omp_get_wtime();
            if (thread == 1) {
                t = t2 - t1;
            }
            acceleration = t / (t2 - t1);
            printf("|\t%9lu\t|\t%9lu\t|\t%7.2f\t\t|\t%9.2f\t|\t%9lu\t|\n", s, k, t2 - t1, acceleration, thread);
            free_dp(dp);
        }
    }
    return 0;
}