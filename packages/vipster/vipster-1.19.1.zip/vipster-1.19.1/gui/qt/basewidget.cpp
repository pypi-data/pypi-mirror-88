#include "basewidget.h"
#include "mainwindow.h"
#include "vipster/global.h"
#include <QApplication>

using namespace Vipster;

BaseWidget::BaseWidget(QWidget* parent)
    :QWidget{parent}
{
    for(auto *w: qApp->topLevelWidgets()){
        if(auto *t = qobject_cast<MainWindow*>(w)){
            master = t;
            return;
        }
    }
    throw Error("Could not determine MainWindow-instance.");
}

void BaseWidget::triggerUpdate(GUI::change_t change)
{
    updateTriggered = true;
    master->updateWidgets(change);
    updateTriggered = false;
}
