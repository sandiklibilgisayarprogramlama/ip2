# pip install flask
# pip install peewee

import datetime
from flask import Flask,request,redirect,session
from flask.helpers import flash, url_for
from flask.templating import render_template
from database import Kullanici, Notlar
from werkzeug.security import generate_password_hash, check_password_hash
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

app=Flask(__name__)
app.secret_key="06e3af3ce8e1d5030e581fd8f038de3810ea16b7b9ea586c"

@app.route("/",methods=["POST","GET"])
def anasayfa():
    # POST işleminde giriş yap gerçekleşiyor
    if request.method=="POST":
        kadi = request.form.get("inp_email")
        sifre = request.form.get("inp_sifre")
        query=Kullanici.select().where((Kullanici.kullaniciadi==kadi)).limit(1)
        gelenad=""
        hash_sifre=""
        kullaniciad=""
        for row in query:
            gelenad = row.adsoyad
            hash_sifre = row.sifre
            kullaniciad=row.kullaniciadi
        if gelenad!="" and check_password_hash(hash_sifre,sifre):
            session["kadi"] = kullaniciad
            return redirect("tumnotlar")
        else:
            return render_template("index.html",hata="girilen kullanıcı adı veya şifre yanlış")
        
    return render_template("index.html")

@app.route("/arama",methods=["POST"])
def arama():
    if "kadi" in session:
        if request.method=="POST":
            arama_metni = request.form.get("inp_arama")
            sonuc = Notlar.select().where(Notlar.baslik.contains(arama_metni.replace("İ","I").lower()))

            return render_template("arama_sonuclari.html",aramasonuclari=sonuc)
    else:
        return redirect("/")


@app.route("/sil/<id>",methods=["GET"])
def sil(id):
    if "kadi" in session:
        result= Notlar.delete_by_id(id)
        if result:
            flash("Not başarıyla silindi !",category="alert alert-success")
        else:
            flash("Silme esnasında bir problem var !",category="alert alert-danger")

        return redirect("/tumnotlar")
    else:
        return redirect("/")

@app.route("/guncelle/<id>",methods=["GET","POST"])
def guncelle(id):
    if "kadi" in session:
        if request.method=="POST":
            yeni_baslik=request.form.get("inp_baslik")
            yeni_icerik=request.form.get("txt_icerik")
            today = datetime.time()
            query = Notlar.update(baslik=yeni_baslik,icerik=yeni_icerik,yayintarihi=today).where(Notlar.id == id)
            query.execute() 
            return redirect("/tumnotlar")

        sonuc = Notlar.select().where(Notlar.id==id)
        return render_template("guncelle.html",guncellenecek = sonuc)
    else:
        return redirect("/")

@app.route("/notekle",methods=["POST","GET"])
def notekle():
    if "kadi" in session:
        if request.method=="POST":
            gelenbaslik = request.form.get("inp_baslik")
            gelenicerik = request.form.get("txt_icerik")
            note = Notlar.create(baslik=gelenbaslik,icerik=gelenicerik,yayintarihi=datetime.time())
            note.save()
            return redirect("/tumnotlar")
        
        return render_template("notekle.html")
    else:
        return redirect("/")

@app.route("/tumnotlar")
def tumnotlar():
    if "kadi" in session:
        notes=Notlar.select()
        return render_template("tumnotlar.html",notlar=notes)
    else:
        return redirect("/")

@app.route("/cikis")
def cikis():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")

@app.route("/kayitol",methods=["POST","GET"])
def kayitol():
    error=""
    if request.method=="POST":
        adsoyad = request.form.get("inp_adsoyad")
        kadi = request.form.get("inp_eposta")
        sifre = request.form.get("inp_pass")
        sifretekrar = request.form.get("inp_repass")
        if sifre == sifretekrar:
            user = Kullanici.create(adsoyad=adsoyad,kullaniciadi=kadi,sifre=generate_password_hash(sifre))
            user.save()
            return redirect("/")
        else:
            error = "Girilen Şifreler birbiri ile uyuşmuyor"
    return render_template("kayit.html",hata = error)

if __name__ == "__main__":
    app.run(debug=True)