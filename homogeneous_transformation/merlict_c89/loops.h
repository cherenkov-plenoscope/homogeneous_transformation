/* Copyright 2018-2020 Sebastian Achim Mueller */
#ifndef LOOP_H_
#define LOOP_H_

#include "chk_debug.h"
#include "mliVec.h"
#include "mliHomTra.h"

int mliHomTraComp_transform(
        const struct mliHomTraComp t_comp,
        const double* vec_in,
        double* vec_out,
        uint64_t num_vec,
        const uint64_t mode)
{
        struct mliVec (*f)(const struct mliHomTra *, const struct mliVec);
        uint64_t i;
        switch (mode) {
                case 0:
                        f = &mliHomTra_pos;
                        break;
                case 1:
                        f = &mliHomTra_pos_inverse;
                        break;
                case 2:
                        f = &mliHomTra_dir;
                        break;
                case 3:
                        f = &mliHomTra_dir_inverse;
                        break;
                default:
                        chk_bad("Mode of transformation is unknown");
                break;
        };

        const struct mliHomTra t = mliHomTra_from_compact(t_comp);
        for (i = 0; i < num_vec; i++) {
                struct mliVec vi, vo;
                vi.x = vec_in[3*i + 0];
                vi.y = vec_in[3*i + 1];
                vi.z = vec_in[3*i + 2];
                vo = f(&t, vi);
                vec_out[3*i + 0] = vo.x;
                vec_out[3*i + 1] = vo.y;
                vec_out[3*i + 2] = vo.z;
        }
        return 1;
error:
        return 0;
}

#endif
