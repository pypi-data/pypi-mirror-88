#include "poscar.h"

#include <sstream>

using namespace Vipster;

static Preset makePreset()
{
    return {&Plugins::Poscar,
        {{"selective", {true, "Toggles selective dynamics.\n\nIf 'true', "
                    "atom-coordinates can be kept fixed during simulation."}},
         {"cartesian", {false, "Toggle between cartesian (Å) and direct (crystal) coordinates."}}}};
}

IOTuple PoscarParser(const std::string& name, std::istream &file){
    Molecule m{name, 1};
    Step &s = m.getStep(0);
    s.setFmt(AtomFmt::Crystal);

    std::string line, tmp;
    size_t n;
    std::stringstream ss;
    std::vector<std::string> types;
    std::vector<size_t> n_per_type;
    bool selective{false};
    double alat;
    auto readline = [&](){
        if(!std::getline(file, line)){
            throw IOError{"POSCAR: file is missing necessary lines."};
        }
        ss = std::stringstream{line};
    };
    // line 1: comment
    readline();
    s.setComment(line);
    /* line 2: scaling
     * positive: direct factor
     * negative: target volume
     */
    readline();
    ss >> tmp;
    alat = std::stod(tmp);
    // lines 3-5: cell vectors
    Mat cell{};
    for(size_t i=0; i<3; ++i){
        readline();
        ss >> cell[i][0] >> cell[i][1] >> cell[i][2];
        if(ss.fail()){
            throw IOError{"POSCAR: invalid cell vectors"};
        }
    }
    s.setCellDim(1, AtomFmt::Angstrom);
    s.setCellVec(cell);
    // atom types (optional), then number of atom per type
    readline();
    ss >> tmp;
    if(ss.fail()){
        throw IOError{"POSCAR: file is missing type information"};
    }
    if(!std::isdigit(tmp[0])){
        // atom types
        types.push_back(tmp);
        ss >> tmp;
        while(!ss.fail()){
            types.push_back(tmp);
            ss >> tmp;
        }
        readline();
        ss >> tmp;
    }
    // register first number of atoms that has been prefetched
    n_per_type.push_back(std::stoul(tmp));
    while(!ss.eof()){
        // register rest of cumulative numbers of atoms
        ss >> n;
        n_per_type.push_back(n+n_per_type.back());
    }
    // make sure number of types add up
    if(!types.empty()){
        if(types.size() != n_per_type.size()){
            throw IOError{"POSCAR: mismatching number of atom types"};
        }
    }else{
        types.reserve(n_per_type.size());
        std::vector<int> tmp(n_per_type.size());
        std::iota(tmp.begin(), tmp.end(), 1);
        for(const auto& i: tmp){
            types.push_back(std::to_string(i));
        }
    }
    // optional: selective-keyword
    // mandatory: selecting between cartesian or 'direct' aka crystal coordinates
    readline();
    if(std::tolower(line[0]) == 's'){
        selective = true;
        readline();
    }
    if(std::tolower(line[0]) == 'c' || std::tolower(line[0]) == 'k'){
        s.setFmt(AtomFmt::Angstrom);
    }
    // atom coordinates: 3 double columns, if selective 3 columns with T or F
    n = 0;
    std::array<char, 3> sel;
    for(size_t i=0; i<n_per_type.back(); ++i){
        s.newAtom(types[n]);
        if(s.getNat() == n_per_type[n]) n++;
        readline();
        auto at = s[i];
        ss >> at.coord[0] >> at.coord[1] >> at.coord[2];
        if(selective){
            ss >> sel[0] >> sel[1] >> sel[2];
            if(sel[0] == 'F') at.properties->flags[AtomProperties::FixX] = true;
            if(sel[1] == 'F') at.properties->flags[AtomProperties::FixY] = true;
            if(sel[2] == 'F') at.properties->flags[AtomProperties::FixZ] = true;
        }
    }

    // finally, scale coordinates with scaling factor
    if(alat < 0){
        // target volume given, calculate real alat here
        double vol = Mat_det(cell);
        alat = -alat/vol;
    }
    s.setCellDim(alat, AtomFmt::Angstrom, true);

    return {std::move(m), std::optional<Parameter>{}, DataList{}};
}

bool PoscarWriter(const Molecule& m, std::ostream &file,
                  const std::optional<Parameter>&,
                  const std::optional<Preset>& c,
                  size_t index)
{
    if(!c || c->getFmt() != &Plugins::Poscar){
        throw IOError("POSCAR: writer needs suitable IO preset");
    }
    auto cartesian = std::get<bool>(c->at("cartesian").first);
    auto selective = std::get<bool>(c->at("selective").first);
    const auto& s = m.getStep(index).asFmt(cartesian ?
                                                 AtomFmt::Angstrom : AtomFmt::Crystal);
    file << s.getComment() << '\n';
    file << s.getCellDim(AtomFmt::Angstrom) << '\n';
    file << std::fixed << std::setprecision(10);
    for(size_t i=0; i<3; ++i){
        const auto& v = s.getCellVec()[i];
        file << v[0] << ' ' << v[1] << ' ' << v[2] << '\n';
    }
    // collect atoms sorted by their type
    std::map<std::string, std::vector<size_t>> types;
    for(auto it=s.begin(); it!=s.end(); ++it){
        types[it->name].push_back(it.getIdx());
    }
    // print out names of types
    for(const auto& type: types){
        file << ' ' << type.first;
    }
    file << '\n';
    // print out number of atoms per type
    for(const auto& type: types){
        file << ' ' << type.second.size();
    }
    file << '\n';
    // print config options
    if(selective){
        file << "Selective\n";
    }
    if(cartesian){
        file << "Cartesian\n";
    }else{
        file << "Direct\n";
    }
    // print atoms
    auto it = s.begin();
    if(selective){
        for(const auto& type: types){
            for(const auto& idx: type.second){
                it += idx-it.getIdx();
                file << ' ' << it->coord[0]
                     << ' ' << it->coord[1]
                     << ' ' << it->coord[2]
                     << ' ' << (it->properties->flags[AtomProperties::FixX] ? 'F' : 'T')
                     << ' ' << (it->properties->flags[AtomProperties::FixY] ? 'F' : 'T')
                     << ' ' << (it->properties->flags[AtomProperties::FixZ] ? 'F' : 'T')
                     << '\n';
            }
        }
    }else{
        for(const auto& type: types){
            for(const auto& idx: type.second){
                it += idx-it.getIdx();
                file << ' ' << it->coord[0]
                     << ' ' << it->coord[1]
                     << ' ' << it->coord[2] << '\n';
            }
        }
    }
    return true;
}

const Plugin Plugins::Poscar =
{
    "VASP POSCAR",
    "POSCAR",
    "pos",
    &PoscarParser,
    &PoscarWriter,
    nullptr,
    &makePreset,
};
