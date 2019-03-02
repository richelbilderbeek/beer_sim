#ifndef GAME_DIALOG_H
#define GAME_DIALOG_H

#include <QDialog>

namespace Ui {
  class game_dialog;
}

class game_dialog : public QDialog
{
  Q_OBJECT

public:
  explicit game_dialog(QWidget *parent = 0);
  ~game_dialog();

private:
  Ui::game_dialog *ui;
};

#endif // GAME_DIALOG_H
