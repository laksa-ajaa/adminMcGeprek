import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,redirect, url_for, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    makanan = list(db.makanan.find({}))
    minuman = list(db.minuman.find({}))
    return render_template('index.html', makanan = makanan, minuman = minuman)

# Makanan
@app.route('/makan', methods=['GET','POST'])
def makan():
    makanan = list(db.makanan.find({}))
    return render_template('makanan.html', makanan = makanan)

@app.route('/tbhmakan', methods=['GET','POST'])
def tbhmakan():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']
        print(nama, harga, deskripsi)
        
        if gambar:
            nama_file  = gambar.filename
            file_path = f'static/assets/img/makanan/{nama_file}'
            gambar.save(file_path)
        else:
            gambar = None

        doc = {
            'nama': nama,
            'harga': harga,
            'gambar': nama_file,
            'deskripsi': deskripsi
        }
        db.makanan.insert_one(doc)
        return redirect(url_for('makan'))
    return render_template('tambahmakan.html')

@app.route('/editmakan/<_id>', methods=['GET','POST'])
def editmakan(_id):
    if request.method == 'POST':
        id = ObjectId(_id)
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi
        }
        
        if gambar:
            nama_file  = gambar.filename
            file_path = f'static/assets/img/makanan/{nama_file}'
            gambar.save(file_path)
            doc['gambar'] = nama_file
        
        db.makanan.update_one({'_id': id}, {'$set': doc})
        return redirect(url_for('makan'))
        
    id = ObjectId(_id)
    data = list(db.makanan.find({'_id': id}))
    return render_template('editmakan.html', data = data)

@app.route('/hapusmakan/<_id>', methods=['GET'])
def hapusmakan(_id):
    db.makanan.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('makan'))

# Minuman
@app.route('/minum', methods=['GET','POST'])
def minum():
    minuman = list(db.minuman.find({}))
    return render_template('minuman.html', minuman = minuman)

@app.route('/tbhminum', methods=['GET','POST'])
def tbhminum():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']
        print(nama, harga, deskripsi)
        
        if gambar:
            nama_file  = gambar.filename
            file_path = f'static/assets/img/minuman/{nama_file}'
            gambar.save(file_path)
        else:
            gambar = None

        doc = {
            'nama': nama,
            'harga': harga,
            'gambar': nama_file,
            'deskripsi': deskripsi
        }
        db.minuman.insert_one(doc)
        return redirect(url_for('minum'))
    return render_template('tambahminum.html')

@app.route('/editminum/<_id>', methods=['GET','POST'])
def editminum(_id):
    if request.method == 'POST':
        id = ObjectId(_id)
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi
        }
        
        if gambar:
            nama_file  = gambar.filename
            file_path = f'static/assets/img/minuman/{nama_file}'
            gambar.save(file_path)
            doc['gambar'] = nama_file
        
        db.minuman.update_one({'_id': id}, {'$set': doc})
        return redirect(url_for('minum'))
        
    id = ObjectId(_id)
    data = list(db.minuman.find({'_id': id}))
    return render_template('editminum.html', data = data)

@app.route('/hapusminum/<_id>', methods=['GET'])
def hapusminum(_id):
    db.minuman.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('minum'))

if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)