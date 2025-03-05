import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Koneksi ke database
conn = sqlite3.connect('sekolah.db')
c = conn.cursor()

# Buat tabel siswa
c.execute('''
    CREATE TABLE IF NOT EXISTS siswa (
        
        nama TEXT,
        Pangkat TEXT,
        nrp TEXT,
        jurusan TEXT,
        tahun TEXT
    );
''')

# Buat tabel guru
c.execute('''
    CREATE TABLE IF NOT EXISTS guru (
        
        nama TEXT,
        pangkat TEXT,
        nrp TEXT,
        mata_pelajaran TEXT
        
    );
''')

# Fungsi untuk menyimpan data siswa
def simpan_siswa(nama, pangkat,nrp, jurusan, tahun ):
    c.execute("INSERT INTO siswa (nama, pangkat,nrp,jurusan,tahun) VALUES (?, ?, ?,?,?)", (nama, pangkat,nrp, jurusan, tahun))
    conn.commit()
# Fungsi untuk menyimpan data guru
def simpan_guru(nama, pangkat,nrp, mata_pelajaran ):
    c.execute("INSERT INTO guru (nama, mata_pelajaran,nrp, pangkat) VALUES (?, ?, ?,?)", (nama, mata_pelajaran,nrp, pangkat))
    conn.commit()
def search_data(query):
    c.execute('SELECT * FROM siswa WHERE nrp  LIKE ?', ('%' + query + '%',))
    return c.fetchall()
def delete_data(nrp):
    c.execute('DELETE FROM siswa WHERE nrp = ?', (nrp,))
    conn.commit()




# Judul aplikasi
st.title("Aplikasi Wingdikum 500", anchor ="#")

# Menu navigasi
with st.sidebar.title("Menu"):
    
    st.header("APLIKASI DATA SISWA WING PENDIDIKAN  500 UMUM ", divider = True)
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVXMlvwvKRpGjw9CC9VpdxQCMfA-gBlZAbiQ&s"
    response =requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    st.sidebar.image(image)
    

    menu =st.sidebar.selectbox("Pilih menu", ["Data Siswa", "Data Gangri", "Tambah Siswa", "Tambah Gangri","Informasi"])
     

    if st.sidebar.button("Buka Link Folder Materi pelajaran"):
        link = "https://drive.google.com/drive/folders/1PKtOMKqF6_hTsBJDXEO-7ms2U-N8IJpU"
        st.sidebar.markdown(link)

                 
     

if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False
if 'deleted' not in st.session_state:
    st.session_state.deleted = False
    


# Data siswa
if menu == "Data Siswa":
    st.write("Pencarian Data")
    
# Buat form pencarian
    search_query = st.text_input("Masukkan NRP Siswa")
    search_button = st.button("Cari")
    
# Tampilkan hasil pencarian
    if search_button:
      results = search_data(search_query)
      st.write("Hasil Pencarian")
      for result in results:
        st.write(f"nama: {result[0]}, pangkat: {result[1]}, nrp: {result[2]}, jurusan: {result[3]},tahun : {result[4]}")
    else :
        st.write("Tidak ditemukan data dengan NRP tersebut")


    st.header("Data Siswa ")
    data_siswa = pd.read_sql_query("SELECT * FROM siswa", conn)
    st.dataframe(data_siswa.style.applymap(lambda x: 'font-size: 18px; font-family: Arial;'), width=1000, height=300,)
    # Fungsi pencarian
    

    
    if st.button("Hapus"):
           st.session_state.deleted = True
    if st.session_state.deleted:
           st.warning("apakah anda yakin")
           if st.button("konfirm"):
                st.session_state.confirmed = True
                st.session_state.deleted = False
                delete_data(search_query)

                conn.commit()
                
           if st.button("batal"):
               st.session_state.deleted = False
    if st.session_state.confirmed:
           st.success("data telah dihapus")
           st.session_state.confirmed = False
    
# Data guru
elif menu == "Data Gangri":
    st.header("Data Gangri")
    data_guru = pd.read_sql_query("SELECT * FROM guru", conn)
    st.write("""
<div style="width:1500px; height:500px; overflow:auto;">
    {}
</div>
""".format(data_guru.to_html()), unsafe_allow_html=True)

# Tambah siswa
elif menu == "Tambah Siswa":
    st.header("Tambah Siswa")
    nama = st.text_input("Nama")
    pangkat = st.text_input("pangkat")
    nrp = st.text_input("nrp")
    jurusan = st.text_input("jurusan")
    tahun = st.text_input("tahun")
    if st.button("Simpan"):
        simpan_siswa(nama, pangkat,nrp, jurusan,tahun)
        st.success("Data siswa berhasil disimpan!")
                 
elif menu == "Tambah Gangri":
    st.header("Tambah Gangri")
    pangkat = st.text_input("pangkat")
    nrp = st.text_input("nrp")
    nama = st.text_input("Gangri")
    mata_pelajaran = st.text_input("Mata Pelajaran")
   
    if st.button("Simpan"):
        simpan_guru(nama,pangkat,nrp, mata_pelajaran)
        st.success("Data guru berhasil disimpan!")

elif menu == "Informasi":
    st.header("Informasi dan Bantuan  ",divider = True)
    image_url1 = "https://github.com/derryjb1/streamlit.wingdikum500/blob/main/derry.jpg?raw=true"
    responses =requests.get(image_url1)
    image1 = Image.open(BytesIO(responses.content))
    st.image(image1)
 
    st.subheader("Nama : Mayor Kes Derry JB",
divider = True)
    st.write("""
# Apabila di temukan masalah pada Aplikasi
silahkan mengirimkan email ke Dayri009@gmail.com""")



