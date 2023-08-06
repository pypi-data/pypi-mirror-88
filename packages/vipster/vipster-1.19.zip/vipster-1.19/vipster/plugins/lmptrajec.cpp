#include "lmptrajec.h"

#include <sstream>

using namespace Vipster;

auto IdentifyColumns(std::string& line)
{
    std::stringstream ss{line};
    std::string tok;
    //throw away "ITEM: ATOMS"
    ss >> tok >> tok;
    enum coordstate{none=0, unscaled=1, scaled=2};
    coordstate cs{};
    auto xparser = [](std::stringstream& ss, Step::atom& at) {ss >> at.coord[0];};
    auto yparser = [](std::stringstream& ss, Step::atom& at) {ss >> at.coord[1];};
    auto zparser = [](std::stringstream& ss, Step::atom& at) {ss >> at.coord[2];};
    auto nparser = [](std::stringstream& ss, Step::atom& at) {ss >> at.name;};
    auto qparser = [](std::stringstream& ss, Step::atom& at) {ss >> at.properties->charge;};
    auto dparser = [](std::stringstream& ss, Step::atom&) {static std::string dummy{}; ss >> dummy;};
    std::vector<void(*)(std::stringstream&, Step::atom&)> funvec{};
    while ( !(ss >> tok).fail() ) {
        if (tok[0] == 'x' || tok[0] == 'y' || tok[0] == 'z') {
            if ((tok.length() == 1) || (tok[1] != 's')) {
                cs = static_cast<coordstate>(cs | unscaled);
            } else if (tok[1] == 's') {
                cs = static_cast<coordstate>(cs | scaled);
            }
            if(tok[0] == 'x') {
                funvec.push_back(xparser);
            } else if(tok[0] == 'y') {
                funvec.push_back(yparser);
            } else if(tok[0] == 'z') {
                funvec.push_back(zparser);
            }
        } else if (tok == "q") {
            funvec.push_back(qparser);
        } else if (tok == "element") {
            funvec.push_back(nparser);
        } else {
            funvec.push_back(dparser);
        }
    }
    switch (static_cast<size_t>(cs)) {
    case unscaled:
        [[fallthrough]];
    case scaled:
        return [=](std::istream &file, Step& s){
            if(cs == scaled) {
                s.setFmt(AtomFmt::Crystal);
            } else {
                s.setFmt(AtomFmt::Angstrom);
            }
            std::string line;
            for (auto& at:s) {
                std::getline(file, line);
                std::stringstream ss{line};
                for (auto& fun:funvec) {
                    fun(ss, at);
                }
                if(ss.fail()) {
                    throw IOError("Lammps Dump: failed to parse atom");
                }
            }
        };
    case unscaled|scaled:
        throw IOError("Lammps Dump: mixed coordinates not supported");
    case none:
        [[fallthrough]];
    default:
        throw IOError("Lammps Dump: no coordinates present");
    }
}

IOTuple LmpTrajecParser(const std::string& name, std::istream &file)
{
    enum class ParseMode{Header, Cell, Atoms};

    Molecule m{name, 0};
    Step* s = nullptr;

    std::string line;
    size_t nat;
    Mat cell;
    while (std::getline(file, line)) {
        if (line.find("TIMESTEP") != std::string::npos) {
            s = &m.newStep();
            // skip 2 lines
            std::getline(file, line);
            std::getline(file, line);
            // Number of Atoms
            std::getline(file, line);
            std::stringstream ss{line};
            ss >> nat;
            if (ss.fail()) {
                throw IOError("Lammps Dump: failed to parse nat");
            }
            s->newAtoms(nat);
            s->setCellDim(1, AtomFmt::Angstrom);
            // Cell
            cell = Mat{};
            std::getline(file, line);
            if ((line.length() > 17) && (line[17] == 'x')) {
                Mat tmp{};
                // xlo_bound, xhi_bound, xy
                std::getline(file, line);
                ss = std::stringstream{line};
                ss >> tmp[0][0] >> tmp[0][1] >> tmp[0][2];
                // ylo_bound, yhi_bound, xz
                std::getline(file, line);
                ss = std::stringstream{line};
                ss >> tmp[1][0] >> tmp[1][1] >> tmp[1][2];
                // zlo, zhi, yz
                std::getline(file, line);
                ss = std::stringstream{line};
                ss >> tmp[2][0] >> tmp[2][1] >> tmp[2][2];
                // untangle lammps' boundary mess
                // xlo = xlo_bound - MIN(0, xy, xz, xy+xz)
                tmp[0][0] = tmp[0][0] - std::min({0., tmp[0][2], tmp[1][2], tmp[0][2]+tmp[1][2]});
                // xhi = xhi_bound - MAX(0, xy, xz, xy+xz)
                tmp[0][1] = tmp[0][1] - std::max({0., tmp[0][2], tmp[1][2], tmp[0][2]+tmp[1][2]});
                // ylo = ylo_bound - MIN(0, yz)
                tmp[1][0] = tmp[1][0] - std::min(0., tmp[2][2]);
                // yhi = yhi_bound - MAX(0, yz)
                tmp[1][1] = tmp[1][1] - std::max(0., tmp[2][2]);
                // x = xhi - xlo
                cell[0][0] = tmp[0][1] - tmp[0][0];
                // y = yhi - ylo
                cell[1][1] = tmp[1][1] - tmp[1][0];
                // tilt "factors" can be used directly
                cell[1][0] = tmp[0][2];
                cell[2][0] = tmp[1][2];
                cell[2][1] = tmp[2][2];
                // zlo_bound == zlo, same for zhi. use directly
                cell[2][2] = tmp[2][1] - tmp[2][0];
            } else {
                double t1, t2;
                // xlo, xhi
                std::getline(file, line);
                ss = std::stringstream{line};
                ss >> t1 >> t2;
                cell[0][0] = t2 - t1;
                // ylo, yhi
                std::getline(file, line);
                ss = std::stringstream{line};
                ss >> t1 >> t2;
                cell[1][1] = t2 - t1;
                // zlo, zhi
                std::getline(file, line);
                ss = std::stringstream{line};
                ss >> t1 >> t2;
                cell[2][2] = t2 - t1;
            }
            if (ss.fail()) {
                throw IOError("Lammps Dump: failed to parse box");
            }
            s->setCellVec(cell, (s->getFmt()==AtomFmt::Crystal));
            // Atoms
            std::getline(file, line);
            auto atomParser = IdentifyColumns(line);
            atomParser(file, *s);
        }
    }
    return {std::move(m), std::optional<Parameter>{}, DataList{}};
}

const Plugin Plugins::LmpTrajec =
{
    "Lammps Dump",
    "lammpstrj",
    "dmp",
    &LmpTrajecParser
};
