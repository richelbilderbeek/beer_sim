#include "game_dialog.h"
#include "ui_game_dialog.h"

game_dialog::game_dialog(QWidget *parent) :
  QDialog(parent),
  ui(new Ui::game_dialog)
{
  ui->setupUi(this);
}

game_dialog::~game_dialog()
{
  delete ui;
}
