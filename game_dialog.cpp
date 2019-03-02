#include "game_dialog.h"
#include "ui_game_dialog.h"

game_dialog::game_dialog(QWidget *parent) :
  QDialog(parent),
  ui(new Ui::game_dialog)
{
  ui->setupUi(this);
  this->startTimer(1000);
}

game_dialog::~game_dialog()
{
  delete ui;
}

void game_dialog::mousePressEvent(QMouseEvent *event)
{
  m_beer_state = beer_state::foam;
  ui->label_beer->setPixmap(QPixmap(":/beer_with_foam.png"));
  ui->label_text->setText("Yummie!\nBeer with foam!");
}

void game_dialog::timerEvent(QTimerEvent *event)
{
  if (m_beer_state == beer_state::foam)
  {
    if (std::rand() % 10 == 0)
    {
      m_beer_state = beer_state::no_foam;
      ui->label_beer->setPixmap(QPixmap(":/beer_no_foam.png"));
      ui->label_text->setText("Yuck! Beer\nwithout foam!");
    }
  }

}
