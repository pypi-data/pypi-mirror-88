#ifndef BONDDELEGATE_H
#define BONDDELEGATE_H

#include <QStyledItemDelegate>

class BondDelegate : public QStyledItemDelegate
{
    Q_OBJECT
public:
    BondDelegate(QObject *parent = nullptr);
    QWidget *createEditor(QWidget *parent, const QStyleOptionViewItem &option,
                          const QModelIndex &index) const override;
    void setModelData(QWidget *editor, QAbstractItemModel *model,
                      const QModelIndex &index) const override;
    bool eventFilter(QObject *object, QEvent *event) override;
};

#endif // BONDDELEGATE_H
