from flask import Flask,request,redirect,session,flash,send_from_directory
from flask.templating import render_template
from database import Kullanici
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import os
app=Flask(__name__)
app.secret_key="06e3af3ce8e1d5030e581fd8f038de3810ea16b7b9ea586c"
app.config['UPLOAD_FOLDER']="uploads"
app.config['MAX_CONTENT_PATH']= 10485760
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route("/")
def anasayfa():
    return render_template("index.html")

@app.route("/uyeol",methods=["POST"])
def uyeol():
    error=""
    if request.method=="POST":
        adsoyad = request.form.get("inp_adsoyad")
        sifre = request.form.get("inp_sifre")
        sifretekrar = request.form.get("inp_sifretekrar")
        eposta = request.form.get("inp_email")
        kadi = request.form.get("inp_kadi")
        if sifre == sifretekrar:
            user = Kullanici.create(adsoyad=adsoyad,eposta=eposta,kullaniciadi=kadi,sifre=generate_password_hash(sifre))
            user.save()
            return redirect("/")
        else:
            error = "Girilen Şifreler birbiri ile uyuşmuyor"
    return render_template("index.html",hata = error)

@app.route("/girisyap",methods=["POST"])
def girisyap():
    kadi=request.form.get("inp_kadi")
    sifre=request.form.get("inp_sifre")
    query=Kullanici.select().where((Kullanici.kullaniciadi==kadi)).limit(1)
    gelenad=""
    hash_sifre=""
    kullaniciad=""
    for row in query:
        gelenad = row.adsoyad
        hash_sifre = row.sifre
        kullaniciad=row.kullaniciadi
        profilresmi=row.profilresmi
        adsoyad=row.adsoyad
    if gelenad!="" and check_password_hash(hash_sifre,sifre):
        session["kadi"] = kullaniciad
        session["profilresmi"] = profilresmi
        session["adsoyad"] = adsoyad
        return redirect("/")
    else:
        return render_template("index.html",hata="girilen kullanıcı adı veya şifre yanlış")

"""
Bilgilerim
-----------------------------
"""


@app.route("/bilgilerim")
def admin():
    if "kadi" in session:
        kullanici = Kullanici.select().where(Kullanici.kullaniciadi == session["kadi"]).dicts().get()
        return render_template("bilgilerim.html",kisi=kullanici)

@app.route("/bilgileriguncelle",methods=["POST"])
def bilgileriguncelle():
    ceptel = request.form.get("inp_ceptel")
    sifre = request.form.get("inp_sifre")
    sifretekrar = request.form.get("inp_sifretekrar")
    eposta = request.form.get("inp_eposta")
    adsoyad = request.form.get("inp_adsoyad")
    if sifre!=None and sifretekrar!=None:
        if sifre == sifretekrar:
            query = Kullanici.update(adsoyad=adsoyad,eposta=eposta,ceptel=ceptel,sifre=generate_password_hash(sifre)).where(Kullanici.kullaniciadi == session["kadi"])
            result=query.execute()
        else:
            result = "Girilen Şifreler birbiri ile uyuşmuyor"
    else:
        query = Kullanici.update(adsoyad=adsoyad,eposta=eposta,ceptel=ceptel)
        result=query.execute()

    if result:
        flash("Profil bilgileri başarıyla Güncellendi !",category="alert alert-success")
    else:
        flash("Güncelleme esnasında bir problem var !",category="alert alert-danger")


    return redirect("/bilgilerim")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/profilfotografekle",methods=["POST"])
def profilfotografekle():
    file = request.files['inp_profilphoto']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        query = Kullanici.update(profilresmi=filename).where(Kullanici.kullaniciadi == session["kadi"])
        result=query.execute()
        if result:
            flash("Profil resmi başarıyla Güncellendi !",category="alert alert-success")
        else:
            flash("Güncelleme esnasında bir problem var !",category="alert alert-danger")
        
        return redirect("/bilgilerim")

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/websiteguncelle",methods=["POST"])
def websiteguncelle():
    website = request.form.get("inp_website")
    query = Kullanici.update(websayfasi=website).where(Kullanici.kullaniciadi == session["kadi"])
    result=query.execute()

    if result:
        flash("Web Sayfası başarıyla Güncellendi !",category="alert alert-success")
    else:
        flash("Güncelleme esnasında bir problem var !",category="alert alert-danger")


    return redirect("/bilgilerim")

"""
######### Bilgilerim
"""

"""
BenimSayfam
-------------------------------
"""

@app.route("/benimsayfam")
def benimsayfam():

    return render_template("benimsayfam.html")

"""
######### BenimSayfam
"""


@app.route("/cikis")
def cikis():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")


if __name__ =="__main__":
    app.run(debug=True)