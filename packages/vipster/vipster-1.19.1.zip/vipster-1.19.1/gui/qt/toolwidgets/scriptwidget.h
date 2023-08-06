#ifndef SCRIPTWIDGET_H
#define SCRIPTWIDGET_H

#include <QWidget>
#include "scripthelp.h"
#include "../basewidget.h"
#include "../viewport.h"
#include "guiglobals.h"
#include "vipster/molecule.h"

namespace Ui {
class ScriptWidget;
}

class ScriptWidget : public BaseWidget
{
    Q_OBJECT

public:
    explicit ScriptWidget(QWidget *parent = nullptr);
    ~ScriptWidget() override;
public slots:
    void evalScript();

private slots:
    void on_helpButton_clicked();

public:
    struct OpVec{
        enum class Mode{Direct, Position, Combination};
        Mode mode{Mode::Direct};
        Vipster::Vec v;
        Vipster::AtomFmt fmt;
        bool m1{false}, m2{false};
        size_t id1, id2;
    };
    friend std::istream& operator>>(std::istream&, std::tuple<OpVec&, bool>);
    struct ScriptOp{
        enum class Mode{None, Rotate, Shift, Mirror, Rename, Select, Define};
        std::string line{};
        std::string target{"all"};
        Mode mode{Mode::None};
        double f{1};
        std::string s1{}, s2{};
        OpVec v1{}, v2{}, v3{};
    };
    std::vector<ScriptOp> parse();
    std::pair<bool, Vipster::GUI::change_t> execute(
            const std::vector<ScriptOp>&, Vipster::Step&,
            ViewPort::StepState&);
    Ui::ScriptWidget *ui;
    ScriptHelp *help;
};

#endif // SCRIPTWIDGET_H
