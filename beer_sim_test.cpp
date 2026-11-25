// Tests for Beer Sim
#include <QtTest>

#include "game_dialog.h"

class beer_sim_test : public QObject
{
  Q_OBJECT

private slots:

  void game_dialog_can_be_shown()
  {
    game_dialog d;
    d.show();
    QVERIFY(QTest::qWaitForWindowExposed(&d));
  }

  void game_dialog_responds_to_clicks()
  {
    game_dialog d;
    d.show();
    QVERIFY(QTest::qWaitForWindowExposed(&d));
    for (int i = 0; i != 10; ++i)
    {
      QTest::mouseClick(&d, Qt::LeftButton);
      QTest::qWait(100);
    }
    QVERIFY(d.isVisible());
  }
};

QTEST_MAIN(beer_sim_test)
#include "beer_sim_test.moc"
