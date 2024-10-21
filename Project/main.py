from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QSpinBox, QRadioButton, \
    QComboBox, QPushButton, QMessageBox

from database import Database

viloyatlar = (
    "Toshkent viloyati",
    "Andijon viloyati",
    "Farg‘ona viloyati",
    "Namangan viloyati",
    "Samarqand viloyati",
    "Buxoro viloyati",
    "Navoiy viloyati",
    "Qashqadaryo viloyati",
    "Surxondaryo viloyati",
    "Jizzax viloyati",
    "Sirdaryo viloyati",
    "Xorazm viloyati",
)

kurslar = (
    "1-kurs",
    "2-kurs",
    "3-kurs",
    "4-kurs"
)


class ComboBoxHBox(QHBoxLayout):
    def __init__(self, label):
        super().__init__()

        combo_label = QLabel(label.capitalize() + ":")
        self.combo_box = QComboBox()
        self.combo_box.addItems(viloyatlar if label == "viloyat" else kurslar if label == "kurs" else None)
        self.addWidget(combo_label)
        self.addWidget(self.combo_box)


class RadioButtonHBox(QHBoxLayout):
    def __init__(self, label: str, ):
        super().__init__()

        radio_buttons_label = QLabel(label.capitalize() + ":")
        rb_v_layout = QVBoxLayout()
        self.jins_erkak_rb = QRadioButton("Erkak")
        self.jins_ayol_rb = QRadioButton("Ayol")
        rb_v_layout.addWidget(self.jins_erkak_rb)
        rb_v_layout.addWidget(self.jins_ayol_rb)
        self.addWidget(radio_buttons_label)
        self.addLayout(rb_v_layout)


class SpinBoxHBox(QHBoxLayout):
    def __init__(self, label: str):
        super().__init__()

        input_label = QLabel(label.capitalize() + ":")
        self.input = QSpinBox()
        self.input.setRange(10, 100)
        self.input.setSingleStep(1)
        self.addWidget(input_label)
        self.addWidget(self.input)


class LineEditHBox(QHBoxLayout):
    def __init__(self, label: str):
        super().__init__()

        input_label = QLabel(label.capitalize() + ":")
        self.input = QLineEdit()
        self.addWidget(input_label)
        self.addWidget(self.input)


class Sorovnoma(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("So'rovnoma")

        layout = QVBoxLayout()

        self.ism_h_layout = LineEditHBox("ism")
        layout.addLayout(self.ism_h_layout)

        self.sharif_h_layout = LineEditHBox("sharif")
        layout.addLayout(self.sharif_h_layout)

        self.yosh_h_layout = SpinBoxHBox("yosh")
        layout.addLayout(self.yosh_h_layout)

        self.jins_h_layout = RadioButtonHBox("jins")
        layout.addLayout(self.jins_h_layout)

        self.viloyat_h_box = ComboBoxHBox("viloyat")
        layout.addLayout(self.viloyat_h_box)

        self.telefon_h_layout = LineEditHBox("telefon")
        layout.addLayout(self.telefon_h_layout)

        self.fakultet_h_layout = LineEditHBox("fakultet")
        layout.addLayout(self.fakultet_h_layout)

        self.kurs_h_box = ComboBoxHBox("kurs")
        layout.addLayout(self.kurs_h_box)

        save_button = SaveButton("Saqlash", self)
        layout.addWidget(save_button)

        self.setLayout(layout)

        self.setStyleSheet(
            """
                QWidget {
                    font-size: 22px;
                }
            """
        )


class SaveButton(QPushButton):
    def __init__(self, text, parent: Sorovnoma):
        super().__init__(text)
        self.parent = parent

        self.clicked.connect(self.save)

    def save(self):
        ism = self.parent.ism_h_layout.input.text()
        sharif = self.parent.sharif_h_layout.input.text()
        yosh = self.parent.yosh_h_layout.input.value()
        jins = "Erkak" if self.parent.jins_h_layout.jins_erkak_rb.isChecked() else "Ayol" if self.parent.jins_h_layout.jins_ayol_rb.isChecked() else None
        viloyat = self.parent.viloyat_h_box.combo_box.currentText()
        telefon_raqami = self.parent.telefon_h_layout.input.text()
        fakultet = self.parent.fakultet_h_layout.input.text()
        kurs = self.parent.kurs_h_box.combo_box.currentText()

        if not ism or not sharif or not jins or not telefon_raqami or not fakultet:
            QMessageBox.warning(self.parent, "Ma'lumot yetishmasligi xatosi", "Barcha field-lar majburiy")
            return

        if not ism.isalpha() or not sharif.isalpha():
            QMessageBox.warning(self.parent, "Ma'lumot not valid xatosi", "Ism va sharif faqat harflardan iborat bo'lishi kerak")
            return

        if not ism[0].isupper() or not sharif[0].isupper():
            QMessageBox.warning(self.parent, "Ma'lumot not valid xatosi", "Ism va sharf 1-harflari bosh harf bo'lishi kerak")
            return

        if not ism[1:].islower() or not sharif[1:].islower():
            QMessageBox.warning(self.parent, "Ma'lumot not valid xatosi",
                                "Ism va sharf 1-harflaridan keyingi harflar kichik bo'lishi kerak")
            return

        if telefon_raqami[0] != '+':
            QMessageBox.warning(self.parent, "Ma'lumot not valid xatosi",
                                "Telefon raqami '+' belgisi bilan boshlanishi kerak")
            return

        if not len(telefon_raqami[1:]) == 12 or not telefon_raqami[1:].isnumeric():
            QMessageBox.warning(self.parent, "Ma'lumot not valid xatosi",
                                "Telefon raqami 12 ta raqamdan iborat bo'lishi kerak")
            return

        with Database() as db:
            try:
                query = "INSERT INTO students \
                (first_name, last_name, age, gender, region, phone, faculty, course) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                values = (ism, sharif, yosh, jins, viloyat, telefon_raqami, fakultet, kurs)
                db.cursor.execute(query, values)
                db.conn.commit()
            except Exception as exp:
                QMessageBox.critical(self.parent, "Ma'lumotlarni saqlash xatosi", str(exp))
                return

        QMessageBox.information(self.parent, "Ma'lumotlarni saqlash holati", "Ma'lumotlar saqlandi")

        self.parent.ism_h_layout.input.clear()
        self.parent.sharif_h_layout.input.clear()
        self.parent.yosh_h_layout.input.setValue(10)

        self.parent.jins_h_layout.jins_erkak_rb.setAutoExclusive(False)
        self.parent.jins_h_layout.jins_ayol_rb.setAutoExclusive(False)
        self.parent.jins_h_layout.jins_erkak_rb.setChecked(False)
        self.parent.jins_h_layout.jins_ayol_rb.setChecked(False)
        self.parent.jins_h_layout.jins_erkak_rb.setAutoExclusive(True)
        self.parent.jins_h_layout.jins_ayol_rb.setAutoExclusive(True)

        self.parent.viloyat_h_box.combo_box.setCurrentIndex(0)
        self.parent.telefon_h_layout.input.clear()
        self.parent.fakultet_h_layout.input.clear()
        self.parent.kurs_h_box.combo_box.setCurrentIndex(0)


def main():
    app = QApplication([])
    sorovnoma_oyna = Sorovnoma()
    sorovnoma_oyna.show()
    app.exec_()


if __name__ == "__main__":
    main()
