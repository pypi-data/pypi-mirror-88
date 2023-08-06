#include "pwoutput.h"

#include <sstream>

using namespace Vipster;

IOTuple PWOutParser(const std::string& name, std::istream &file)
{
    Molecule m{name, 1};
    Step *s = &m.getStep(0);

    std::string line, dummy_s;
    size_t nat{}, ntype{};
    double celldim{};
    Mat cellvec;
    bool gamma{false}, readInitial{false};
    AtomFmt cdmfmt{AtomFmt::Bohr};
    std::vector<std::string> pseudopotentials{};
    while (std::getline(file, line)) {
        if (line.find("number of atoms/cell") != std::string::npos) {
            std::stringstream{line.substr(33)} >> nat;
            s->newAtoms(nat);
            std::getline(file, line);
            std::stringstream{line.substr(33)} >> ntype;
        } else if (line.find("gamma-point") != std::string::npos) {
            gamma = true;
        } else if (line.find("number of k points=") != std::string::npos) {
            if (gamma) {
                continue;
            }
            size_t nk = static_cast<size_t>(std::stoi(line.substr(line.find('=')+1)));
            // skip header
            std::getline(file, line);
            // if nk >= 100 and verbosity is not high, k-points are not printed
            std::getline(file, line);
            if(line.find("'high'") != std::string::npos){
                continue;
            }
            // found discrete k-points, parse them
            auto& kpts = m.kpoints;
            kpts.active = KPoints::Fmt::Discrete;
            kpts.discrete.kpoints.resize(nk);
            for (auto& k: kpts.discrete.kpoints) {
                std::stringstream ss{line};
                std::getline(ss, dummy_s, '(');
                std::getline(ss, dummy_s, '(');
                ss >> k.pos[0] >> k.pos[1] >> k.pos[2];
                std::getline(ss, dummy_s, '=');
                ss >> k.weight;
                std::getline(file, line);
            }
        } else if (line.find("celldm(1)=") != std::string::npos) {
            /*
             * parse celldm(1)
             * always given with discrete vectors
             * ibrav and rest of celldm not needed
             */
            std::stringstream{line} >> dummy_s >> celldim;
            s->setCellDim(celldim, cdmfmt);
            // skip to cell-vectors
            std::getline(file, line);
            std::getline(file, line);
            std::getline(file, line);
            for(size_t i=0; i<3; ++i){
                std::getline(file, line);
                std::stringstream{line} >> dummy_s >> dummy_s >> dummy_s
                        >> cellvec[i][0] >> cellvec[i][1] >> cellvec[i][2];
            }
            s->setCellVec(cellvec);
        } else if (line.find("PseudoPot.") != std::string::npos){
            // parse pseudopotential from next line
            std::getline(file, line);
            std::string tmp;
            std::stringstream{line} >> tmp;
            pseudopotentials.emplace_back(tmp.substr(tmp.find_last_of('/')+1));
        } else if ((line.find("atomic species") != std::string::npos) &&
                   (line.find("pseudopotential") != std::string::npos)){
            // parse names, masses and assign corresponding pseudopotential
            for(size_t i=0; i<ntype; ++i){
                std::getline(file, line);
                std::string tmp;
                auto ss = std::stringstream{line};
                ss >> tmp;
                auto& entry = m.getPTE()[tmp];
                ss >> tmp >> tmp;
                entry.m = std::stod(tmp);
                entry.PWPP = pseudopotentials[i];
            }
        } else if (!readInitial && (line.find("site n.") != std::string::npos)) {
            // parse initial coordinates
            // always given as ALAT (or aditionally as CRYSTAL with high verbosity)
            s->setFmt(AtomFmt::Alat);
            for(auto& at: *s){
                std::getline(file, line);
                std::stringstream ss{line};
                ss >> dummy_s >> at.name >> dummy_s;
                std::getline(ss, dummy_s, '(');
                ss >> at.coord[0] >> at.coord[1] >> at.coord[2];
                if (ss.fail()) {
                    throw IOError{"PWScf Output: failed to parse atom"};
                }
            }
            readInitial = true;
        } else if ((line.find("CELL_PARAMETERS") != std::string::npos) &&
                   (line.find("DEPRECATED") == std::string::npos)) {
            if (line.find("(bohr)") != std::string::npos) {
                cdmfmt = AtomFmt::Bohr;
                celldim = 1;
            }else if (line.find("angstrom") != std::string::npos) {
                cdmfmt = AtomFmt::Angstrom;
                celldim = 1;
            }else{
                cdmfmt = AtomFmt::Bohr;
                celldim = std::stod(line.substr(line.find('=')+1));
            }
            // parse vectors
            for(Vec& v: cellvec){
                std::getline(file, line);
                std::stringstream{line} >> v[0] >> v[1] >> v[2];
            }
        } else if (line.find("ATOMIC_POSITIONS") != std::string::npos) {
            // formatted positions
            // creating new step here
            s = &m.newStep();
            s->setCellDim(celldim, cdmfmt);
            s->setCellVec(cellvec);
            s->newAtoms(nat);
            if(line.find("angstrom") != std::string::npos) {
                s->setFmt(AtomFmt::Angstrom);
            }else if (line.find("bohr") != std::string::npos) {
                s->setFmt(AtomFmt::Bohr);
            }else if (line.find("crystal") != std::string::npos) {
                s->setFmt(AtomFmt::Crystal);
            }else{
                s->setFmt(AtomFmt::Alat);
            }
            for(auto& at: *s){
                std::getline(file, line);
                auto linestream = std::stringstream{line};
                linestream >> at.name >> at.coord[0] >> at.coord[1] >> at.coord[2];
                bool x{true}, y{true}, z{true};
                linestream >> x >> y >> z;
                at.properties->flags[AtomProperties::FixX] = !x;
                at.properties->flags[AtomProperties::FixY] = !y;
                at.properties->flags[AtomProperties::FixZ] = !z;
            }
        }
        else if (line.find("Begin final coordinates") != std::string::npos) {
            break;
        }
    }

    return {std::move(m), std::optional<Parameter>{}, DataList{}};
}

const Plugin Plugins::PWOutput =
{
    "PWScf Output File",
    "pwo",
    "pwo",
    &PWOutParser
};
