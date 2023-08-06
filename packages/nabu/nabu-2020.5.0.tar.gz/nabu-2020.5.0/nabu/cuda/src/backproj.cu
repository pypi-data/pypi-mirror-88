#ifndef SHARED_SIZE
    #define SHARED_SIZE 256
#endif

texture<float, 2, cudaReadModeElementType> tex_projections;

#ifdef BACKPROJ3D
texture<float, 3, cudaReadModeElementType> tex_projections3D;
#endif

/**

Implementation details
-----------------------
This implementation uses two pre-computed arrays in global memory:
  cos(theta)  -> d_cos
  -sin(theta) -> d_msin
As the backprojection is voxel-driven, each thread will, at some point,
need cos(theta) and -sin(theta) for *all* theta.
Thus, we need to pre-fetch d_cos and d_msin in the fastest cached memory.
Here we use the shared memory (faster than constant memory and texture).
Each thread group will pre-fetch values from d_cos and d_msin to shared memory
Initially, we fetched as much values as possible, ending up in a block of 1024
threads (32, 32). However, it turns out that performances are best with (16, 16)
blocks.
**/

// Backproject one sinogram
// One thread handles up to 4 pixels in the output slice
// the case num_projs > 1024 has to be included.
__global__ void backproj(
    float* d_slice,
    int num_projs,
    int num_bins,
    #ifdef BACKPROJ3D
    int num_slices,
    #endif
    float axis_position,
    int n_x,
    int n_y,
    int offset_x,
    int offset_y,
    float* d_cos,
    float* d_msin,
    #ifdef DO_AXIS_CORRECTION
    float* d_axis_corr,
    #endif
    float scale_factor
)
{
    int x = offset_x + blockDim.x * blockIdx.x + threadIdx.x;
    int y = offset_y + blockDim.y * blockIdx.y + threadIdx.y;
    #ifdef BACKPROJ3D
    int z = blockDim.z * blockIdx.z + threadIdx.z;
    #endif

    int Gx = blockDim.x * gridDim.x;
    int Gy = blockDim.y * gridDim.y;

    // (xr, yr)    (xrp, yr)
    // (xr, yrp)   (xrp, yrp)
    float xr = x - axis_position, yr = y - axis_position;
    float xrp = xr + Gx, yrp = yr + Gy;

    /*volatile*/ __shared__ float s_cos[SHARED_SIZE];
    /*volatile*/ __shared__ float s_msin[SHARED_SIZE];
    #ifdef DO_AXIS_CORRECTION
    /*volatile*/ __shared__ float s_axis[SHARED_SIZE];
    float axcorr;
    #endif

    int next_fetch = 0;
    int tid = threadIdx.y * blockDim.x + threadIdx.x;

    float costheta, msintheta;
    float h1, h2, h3, h4;
    float sum1 = 0.0f, sum2 = 0.0f, sum3 = 0.0f, sum4 = 0.0f;

    for (int proj = 0; proj < num_projs; proj++) {
        if (proj == next_fetch) {
            // Fetch SHARED_SIZE values to shared memory
            __syncthreads();
            if (next_fetch + tid < num_projs) {
                s_cos[tid] = d_cos[next_fetch + tid];
                s_msin[tid] = d_msin[next_fetch + tid];
                #ifdef DO_AXIS_CORRECTION
                s_axis[tid] = d_axis_corr[next_fetch + tid];
                #endif
            }
            next_fetch += SHARED_SIZE;
            __syncthreads();
        }

        costheta = s_cos[proj - (next_fetch - SHARED_SIZE)];
        msintheta = s_msin[proj - (next_fetch - SHARED_SIZE)];
        #ifdef DO_AXIS_CORRECTION
        axcorr = s_axis[proj - (next_fetch - SHARED_SIZE)];
        #endif
        float c1 = fmaf(costheta, xr, axis_position); // cos(theta)*xr + axis_pos
        float c2 = fmaf(costheta, xrp, axis_position); // cos(theta)*(xr + Gx) + axis_pos
        float s1 = fmaf(msintheta, yr, 0.0f); // -sin(theta)*yr
        float s2 = fmaf(msintheta, yrp, 0.0f); // -sin(theta)*(yr + Gy)
        h1 = c1 + s1;
        h2 = c2 + s1;
        h3 = c1 + s2;
        h4 = c2 + s2;
        #ifdef DO_AXIS_CORRECTION
        h1 += axcorr;
        h2 += axcorr;
        h3 += axcorr;
        h4 += axcorr;
        #endif

        #ifdef BACKPROJ3D
        if (h1 >= 0 && h1 < num_bins) sum1 += tex3D(tex_projections3D, h1 + 0.5f, proj + 0.5f, z + 0.5f);
        if (h2 >= 0 && h2 < num_bins) sum2 += tex3D(tex_projections3D, h2 + 0.5f, proj + 0.5f, z + 0.5f);
        if (h3 >= 0 && h3 < num_bins) sum3 += tex3D(tex_projections3D, h3 + 0.5f, proj + 0.5f, z + 0.5f);
        if (h4 >= 0 && h4 < num_bins) sum4 += tex3D(tex_projections3D, h4 + 0.5f, proj + 0.5f, z + 0.5f);
        #else
        if (h1 >= 0 && h1 < num_bins) sum1 += tex2D(tex_projections, h1 + 0.5f, proj + 0.5f);
        if (h2 >= 0 && h2 < num_bins) sum2 += tex2D(tex_projections, h2 + 0.5f, proj + 0.5f);
        if (h3 >= 0 && h3 < num_bins) sum3 += tex2D(tex_projections, h3 + 0.5f, proj + 0.5f);
        if (h4 >= 0 && h4 < num_bins) sum4 += tex2D(tex_projections, h4 + 0.5f, proj + 0.5f);
        #endif
    }

    x -= offset_x;
    y -= offset_y;

    // useful only if n_x < blocksize_x or n_y < blocksize_y
    if (x >= n_x) return;
    if (y >= n_y) return;

    #ifdef BACKPROJ3D
    d_slice[(z*n_y + y)*(n_x) + x] = sum1 * scale_factor;
    if (Gx + x < n_x)
        d_slice[(z*n_y + y)*(n_x) + Gx + x] = sum2 * scale_factor;
    if (Gy + y < n_y) {
        d_slice[(z*n_y + y + Gy)*(n_x) + x] = sum3 * scale_factor;
    if (Gx + x < n_x)
        d_slice[(z*n_y + y + Gy)*(n_x) + Gx + x] = sum4 * scale_factor;
    }
    #else
    d_slice[y*(n_x) + x] = sum1 * scale_factor;
    if (Gx + x < n_x)
        d_slice[y*(n_x) + Gx + x] = sum2 * scale_factor;
    if (Gy + y < n_y) {
        d_slice[(y+Gy)*(n_x) + x] = sum3 * scale_factor;
    if (Gx + x < n_x)
        d_slice[(y+Gy)*(n_x) + Gx + x] = sum4 * scale_factor;
    }
    #endif
}
