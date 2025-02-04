#include <TVector3.h>
#include <stdio.h>
#include <iostream>

#include "pixel_module_faces_2018.h"
#include "pixel_module_volumes_2018.h"


bool is_point_in_one_module(float px, float py, float pz, float arr[]) {
    float sx = px - arr[9];
    float sy = py - arr[10];
    float sz = pz - arr[11];
    for (unsigned int i = 0; i < 3; i++) {
        if (fabs(arr[3*i]*sx + arr[3*i+1]*sy + arr[3*i+2]*sz) > arr[i+12]) return false;
    }
    return true;
}

bool is_point_in_any_module(float px, float py, float pz) {
    for (unsigned int imodule = 0; imodule < NMODULES; imodule++) {
        if (is_point_in_one_module(px, py, pz, module_volumes[imodule])) return true;
    }
    return false;
}

bool is_ray_inside_face(const TVector3 v[], TVector3 rayorig, TVector3 raydir) {
    auto raydirunit = raydir.Unit();

    auto normal = (v[1]-v[0]).Cross(v[3]-v[0]);
    if (normal.Mag2() < 1e-6) {
        normal = (v[2]-v[1]).Cross(v[3]-v[0]);
    }
    auto normalunit = normal.Unit();

    auto h = (rayorig-v[0]).Dot(normalunit);
    auto dproj = raydirunit.Dot(-normalunit);
    float scale = h/dproj;
    if (scale < 0) return false;
    auto p = rayorig + raydirunit*scale;

    float a0 = (v[0]-p).Cross(v[1]-p).Mag();
    float a1 = (v[1]-p).Cross(v[2]-p).Mag();
    float a2 = (v[2]-p).Cross(v[3]-p).Mag();
    float a3 = (v[3]-p).Cross(v[0]-p).Mag();
    float trec = normal.Mag();

    bool inside = (0.5*(a0+a1+a2+a3) <= trec);
    return inside;
}

int ray_module_crosses(TVector3 rayorig, TVector3 raydir) {
    int ncrosses = 0;
    for (unsigned int imodule = 0; imodule < NMODULES; imodule++) {
        int nhitfaces = 0;
        for (unsigned int iface = 0; iface < NFACES; iface++) {
            if (is_ray_inside_face(module_faces[imodule][iface], rayorig, raydir)) {
                nhitfaces += 1;
                if (nhitfaces >= 2) {
                    ncrosses += 1;
                    break;
                }
            }
        }
    }
    return ncrosses;
}

int calculate_module_crosses(float origx, float origy, float origz,
                          float dirx, float diry, float dirz) {

    auto rayorig = TVector3(origx, origy, origz);
    auto raydir = TVector3(dirx, diry, dirz);

    return ray_module_crosses(rayorig, raydir);

}
