import model
import controller


# 
# Fungsi model
# - mendefinisikan object apa yang perlu ditampilkan Odoo, setelah menu item tertentu di KLIK
#
# Fungsi sql_script
# - agar codingan lebih rapi dan easily re-edit, maka script SQL di pisah dengan script py
#
# Fungsi controller
# - Dashboard harus bisa di print dalam bentuk XLSX yang di-trigger dari Javasript
# - Sehingga, Dashboard harus memiliki Routing sendiri untuk me-return sebuah File XLSX
