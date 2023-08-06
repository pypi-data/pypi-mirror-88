#ifndef MOLMODEL_H
#define MOLMODEL_H

#include <QAbstractTableModel>
#include "vipster/molecule.h"

class MolWidget;
class AtomModel : public QAbstractTableModel
{
    Q_OBJECT

public:
    explicit AtomModel(MolWidget *parent = nullptr);
    void setStep(Vipster::Step::formatter* curStep);
    void setColumns(int cols);

    // Header:
    QVariant headerData(int section, Qt::Orientation orientation,
                        int role = Qt::DisplayRole) const override;

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;

private:
    MolWidget *parent;
    Vipster::Step::formatter* curStep{nullptr};
    QStringList colNames = {"Type" , "x", "y", "z", "Charge", "fx", "fy", "fz",
                            "Hide", "fix x", "fix y", "fix z"};
    std::vector<int> colMap = {0,1,2,3};
};

#endif // MOLMODEL_H
