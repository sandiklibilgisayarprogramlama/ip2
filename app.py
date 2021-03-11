# pip install flask
# pip install peewee

import datetime
from flask import Flask,request,redirect
from flask.templating import render_template
from database import Kullanici, Notlar
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def anasayfa():
    if request.method=="POST":
        kadi = request.form.get("inp_email")
        sifre = request.form.get("inp_sifre")
        query=Kullanici.select().where((Kullanici.kullaniciadi==kadi)\
             and (check_password_hash(Kullanici.sifre,sifre)))
        
        print([user.kullaniciadi for user in query])

        
    return render_template("index.html")

@app.route("/notekle",methods=["POST"])
def notekle():
    if request.method=="POST":
        gelenbaslik = request.form.get("inp_baslik")
        gelenicerik = request.form.get("txt_icerik")
        note = Notlar.create(baslik=gelenbaslik,icerik=gelenicerik,yayintarihi=datetime.time())
        note.save()
        return redirect("/tumnotlar")

@app.route("/tumnotlar")
def tumnotlar():
    notes=Notlar.select()
    return render_template("tumnotlar.html",notlar=notes)

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