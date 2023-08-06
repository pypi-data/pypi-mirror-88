#include "atom.h"

using namespace Vipster;

bool Vipster::atomFmtRelative(AtomFmt f)
{
    return f<=AtomFmt::Alat;
}

bool Vipster::atomFmtAbsolute(AtomFmt f)
{
    return !atomFmtRelative(f);
}

bool Vipster::operator==(const AtomProperties &p1, const AtomProperties &p2)
{
    return std::tie(p1.charge, p1.flags, p1.forces)
           ==
           std::tie(p2.charge, p2.flags, p2.forces);
}

detail::CoordConverter Vipster::detail::makeConverter(const AtomContext &source,
                                                      const AtomContext &target)
{
    switch(source.fmt){
    case AtomFmt::Crystal:
        switch(target.fmt){
        case AtomFmt::Crystal:
            if(source.cell == target.cell){
                return [](const Vec &v){return v;};
            }else{
                return [&](const Vec &v){return v * (source.cell->matrix * source.cell->dimension)
                                                  * (target.cell->inverse / target.cell->dimension);};
            }
        case AtomFmt::Alat:
            return [&](const Vec &v){return v * (source.cell->matrix * source.cell->dimension)
                                              / target.cell->dimension;};
        default:
            return [&](const Vec &v){return v * (source.cell->matrix * source.cell->dimension)
                                              * detail::AtomContext::fromAngstrom[target.fmt];};
        }
    case AtomFmt::Alat:
        switch(target.fmt){
        case AtomFmt::Crystal:
            if(source.cell->dimension == target.cell->dimension){
                return [&](const Vec &v){return v * target.cell->inverse;};
            }else{
                return [&](const Vec &v){return v * source.cell->dimension
                                                  * (target.cell->inverse / target.cell->dimension);};
            }
        case AtomFmt::Alat:
            if(source.cell->dimension == target.cell->dimension){
                return [](const Vec &v){return v;};
            }else{
                return [&](const Vec &v){return v * source.cell->dimension / target.cell->dimension;};
            }
        default:
            return [&](const Vec &v){return v * source.cell->dimension
                                              * detail::AtomContext::fromAngstrom[target.fmt];};
        }
    default: // absolute coordinates
        switch(target.fmt){
        case AtomFmt::Crystal:
            return [&](const Vec &v){return v * detail::AtomContext::toAngstrom[source.fmt]
                                              * (target.cell->inverse / target.cell->dimension);};
        case AtomFmt::Alat:
            return [&](const Vec &v){return v * detail::AtomContext::toAngstrom[source.fmt]
                                              / target.cell->dimension;};
        default:
            if(source.fmt == target.fmt){
                return [](const Vec &v){return v;};
            }else{
                return [&](const Vec &v){return v * detail::AtomContext::toAngstrom[source.fmt]
                                                  * detail::AtomContext::fromAngstrom[target.fmt];};
            }
        }
    }
}
