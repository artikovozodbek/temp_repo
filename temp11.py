import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zakovat Quiz")
        self.resize(700, 500)

        self.layout = QVBoxLayout()

        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)

        self.timer_label = QLabel("Vaqt: 90")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setObjectName("timerLabel")

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Javobingizni kiriting...")
        self.answer_input.setMinimumHeight(50)

        self.submit_button = QPushButton("Javobni yuborish")
        self.submit_button.clicked.connect(self.check_answer)

        self.answer_input.returnPressed.connect(self.check_answer)

        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.answer_input)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        # 🎨 SOFT DESIGN
        self.setStyleSheet("""
        QWidget {
            background-color: #121212;
        }

        QLabel {
            color: #e1e1e1;
            font-size: 25px;
            font-weight: bold;
        }

        #timerLabel {
            color: #4da6ff;
            font-size: 24px;
        }

        QLineEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #333;
        }

        QLineEdit:focus {
            border: 1px solid #4da6ff;
        }

        QPushButton {
            background-color: #4da6ff;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 8px;
        }

        QPushButton:hover {
            background-color: #3399ff;
        }

        QPushButton:pressed {
            background-color: #267acc;
        }
        """)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # ✅ 12 ta savol
        self.questions = [
            ("Bu multfilm yaratuvchilaridan biri bo‘lgan Aleksandr Tatarskiy shunday deydi: "
             "“Besh yoshlik vaqtimda turli qurilmalar ichida kim yashashi menga juda qiziq edi”. "
             "Savol: Tatarskiy qaysi multfilm yaratuvchilaridan biri?",
             ["fiksiklar", "fiksik"]),

            ("Xayrulla Hamidov ijodidan sheʼrni tinglang: Ha seni insoniy mardiliging edi "
             "Barchani teng ko‘rib, ters yurmasliging Va lekin eng mushkul yumushing boshqa "
             "Hayvonlar ichida o‘zgarmasliging! Savol: Ushbu sheʼr qaysi adabiy personaj nomi bilan atalgan?",
             ["maugli"]),

            ("1959-yildan 1960-yil avgust oyigacha amalda bo‘lgan Gabon davlati bayrog‘ining markazida "
             "ingichka sariq chiziqni ko‘rish mumkin edi. Bayroqdagi ko‘k rang Atlantika okeanini bildirgan. "
             "Savol: Sariq chiziq nimani ifodalaydi?",
             ["ekvator"]),

            ("1982-yil Folklend urushi paytida inglizlar ularni dushman suvosti kemalari deb o‘ylab "
             "ulardan uchtasini o‘ldirishgan. Wikipedia ma’lumotiga ko‘ra, begemotlar ularning "
             "quruqlikdagi eng yaqin qarindoshlari hisoblanadi. Savol: Ular nima?",
             ["kit", "kitlar"]),

            ("Bu shirinlik Xitoyda miloddan avvalgi 206–220 yillarda paydo bo‘lgan. "
             "Xitoyliklar bu shirinlikni 'ajdar soqoli' deb atashgan. "
             "Savol: Bu shirinlik nomi nima?",
             ["paxtaqand"]),
             

            ("Mo‘g‘ul xalqida bizda ham mavjud bo‘lgan iboraning davomi mavjud. "
             "Iborada hech qachon echkining shoxlari osmonga yetmasligi aytiladi. "
             "Savol: Bizdagi iborada qaysi jonzot tilga olinadi?",
             ["tuya"]),

            ("Savol matnida bir so‘zdan harflar tushirib qoldirilgan. "
             "Turli xil baliq va dengiz mahsulotlari sotiluvchi Yakutiyadagi bozorda "
             "ehtiyoj yo‘q bo‘lgani uchun ularni ko‘rmaysiz. Ular o‘rtacha 13 yil ishlaydi. "
             "Savol: U nima?",
             ["muzlatgich"]),

            ("U o‘z logotipini o‘zgartirdi. Ranglar sekin asta o‘zgarib ketadi: qizil → sariq → yashil → ko‘k. "
             "Savol: Bu qaysi kompaniya?",
             ["google"]),

            ("XX asr oxirida bo‘lgan voqeadan keyin hayvonlar radiatsiyaga moslashgan. "
             "Masalan, bo‘rilar va qurbaqalar o‘zgargan. "
             "Savol: Bu voqea qayerda bo‘lgan?",
             ["chernobil", "chernobyl"]),

            ("Natalya Mazurning aytishicha, XVIII asr inglizlari uni zahar deb o‘ylashgan. "
             "Savol: U nima?",
             ["choy", "tea"]),

            ("ALFA “fanlar onasi” va “G‘arb falsafasi beshigi” sifatida mashhur. "
             "Savol: ALFA nima?",
             ["afina", "athens"]),

            ("Qadimgi rimliklar mag‘lubiyatni uning jahli bilan bog‘lashgan. "
             "Yana biri shokolad nomi. "
             "Savol: U nima?",
             ["mars"])
        ]

        self.index = 0
        self.correct = 0

        self.load_question()

    def normalize(self, text):
        text = text.casefold().strip()
        text = text.replace("’", "'").replace("ʻ", "'")
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def load_question(self):
        if self.index >= len(self.questions):
            self.finish_test()
            return

        self.time_left = 90
        self.timer_label.setText(f"Vaqt: {self.time_left}")
        self.answer_input.clear()

        question, _ = self.questions[self.index]
        self.question_label.setText(f"{self.index+1}-SAVOL\n\n{question}")

        self.timer.start(1000)

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Vaqt: {self.time_left}")

        if self.time_left <= 10:
            self.timer_label.setStyleSheet("color: #ff6666; font-size: 24px; font-weight: bold;")

        if self.time_left <= 0:
            self.timer.stop()
            QMessageBox.warning(self, "Vaqt tugadi",
                                f"To‘g‘ri javob: {self.questions[self.index][1][0]}")
            self.next_question()

    def check_answer(self):
        self.timer.stop()

        user_answer = self.normalize(self.answer_input.text())
        correct_answers = self.questions[self.index][1]

        if user_answer in [self.normalize(ans) for ans in correct_answers]:
            self.correct += 1
            QMessageBox.information(self, "Natija", "✅ To‘g‘ri")
        else:
            QMessageBox.warning(self, "Natija",
                                f"❌ To‘g‘ri javob: {correct_answers[0]}")

        self.next_question()

    def next_question(self):
        self.index += 1
        self.load_question()

    def finish_test(self):
        total = len(self.questions)
        percent = (self.correct / total) * 100

        self.question_label.setText(
            f"🏁 TEST YAKUNLANDI\n\n"
            f"To‘g‘ri: {self.correct}/{total}\n"
            f"Foiz: {percent:.1f}%"
        )

        self.timer_label.hide()
        self.answer_input.hide()
        self.submit_button.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())

