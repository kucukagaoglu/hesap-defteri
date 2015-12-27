#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb, os, time, sqlite3,datetime
"""
Simple demo of a horizontal bar chart.
"""
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np




## dd/mm/yyyy format
tarih=time.strftime("%Y-%m-%d")
simdi = datetime.datetime.now()
ay=simdi.month

baglanti=sqlite3.connect("/var/www/test/hesap.db")
baglanti.text_factory = str
cur=baglanti.cursor()

form=cgi.FieldStorage()
print ('Content-Type:text/html; charset=windows-1254\n')

cgitb.enable()


print("""
<head>
  <meta charset="utf-8">
  <title>HESAP DEFTERi</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
  <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  <link rel="stylesheet" href="/resources/demos/style.css">
  <script>

$(function() {

      $( "#datepicker" ).datepicker({ dateFormat: 'yy-mm-dd' });

    });	



  </script>
</head>

	""")

print('<html><title>Ekleme</title>')

print("""<style>

body {

background-color:lightgrey ; 
font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;

}

button, input, select, textarea {
  font-family : "Trebuchet MS", Arial, Helvetica, sans-serif;
  font-size   : 100%;
}

#customers {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 80%;
}

#customers td, #customers th {
    border: 1px solid #ddd;
    text-align: left;
    padding: 8px;
}

#customers tr:nth-child(even){background-color: #f2f2f2}

#customers tr:hover {background-color: #ddd;}

#customers th {
    padding-top: 12px;
    padding-bottom: 12px;
    background-color: #4CAF50;
    color: white;
			  }
</style>""")

print ("<fieldset>")
print("<legend> Son harcama</legend>")
print('<table id="customers">')


if(not form.getvalue('adi') or not form.getvalue('miktari') or not form.getvalue('tarihi')):
	print ('<td><b> Lutfen eksiksiz doldur!</b></td>')	

else:
	if form.getvalue('adi'):
		print ('<td><b> Harcama Yeri:</b></td><td>%s</td></tr>' % form['adi'].value)	
	if form.getvalue('miktari'):
		print ('<td><b> Harcama Miktari:</b></td><td>%s TL</td></tr>' % form['miktari'].value)
	if form.getvalue('tarihi'):
		print ('<td><b> Harcama Tarihi:</b></td><td>%s</td></tr>' % form['tarihi'].value)
	if form.getvalue('dropdown'):
		print ('<td><b> Harcama Turu:</b></td><td>%s</td></tr>' % form['dropdown'].value)
	if form.getvalue('aciklama'):
		print ('<td><b> Aciklama:</b></td><td>%s</td></tr>' % form['aciklama'].value)
		

	#-ferek kalmadı--form['tarihi'].value=datetime.datetime.strptime(form['tarihi'].value, '%m/%d/%Y').strftime('%Y-%m-%d')

	cur.execute('''INSERT INTO harcamalar 
		(adi,miktari,tarihi,turu,aciklama) 
		VALUES ("%s","%d","%s","%s","%s")'''
		%(form['adi'].value,int(form['miktari'].value),form['tarihi'].value,form['dropdown'].value,form['aciklama'].value))
#	cur.execute('''INSERT INTO harcamalar ({},{},{},{})'''.format(form['adi'].value,int(form['miktari'].value),form['tarihi'].value,form['dropdown'].value))
	#cur.execute('''INSERT INTO harcamalar ({},{05d},{},{})'''.format("cagdas","55","12/12/2015","market"))
	baglanti.commit()


	print("<body>")
	print("</table>")
	print ('<td><b> Kayit basari ile eklendi!</b></td>')
	print('<meta http-equiv="refresh" content="0; url=ekle.py" />') #birden fazla eklemek icin engel!

print ("</fieldset>")

print("</table>")

print ("<hr>")

print ('<form method="POST">')
print ("<fieldset>")
print("<legend><b> HARCAMA EKLE </legend>")
print('<br>Harcama Yeri:<br> <input type="text" name="adi">')



print('<br>Harcama Miktari: <br><input type="number" name="miktari">')

print("""
	<script	>
$('input[type="number"]').keypress(function(e) {
    var a = [];
    var k = e.which;

    for (i = 48; i < 58; i++)
        a.push(i);

    if (!(a.indexOf(k)>=0))
        e.preventDefault();
});


</script>
	""")


print('<br>Tarih(Ay/Gun/Yil): <br><input data-format="dd-MM-yyyy" type="text" id="datepicker" name="tarihi" </input>') #value=%s>'%tarih)

print ('<br><br>Turu:<br><select name="dropdown">')
print ('<option value="market" selected>market</option>')
print ('<option value="yakit">yakit</option>')
print ('<option value="giyim" >giyim</option>')
print ('<option value="fatura" >fatura</option>')
print ('<option value="hirdavat" >hirdavat</option>')
print ('<option value="cocuk/eglence" >cocuk/eglence</option>')
print ('<option value="aidat" >aidat</option>')
print ('<option value="kultur/sanat/egitim/spor" >kultur/sanat/egitim/spor</option>')
print ('<option value="teknoloji" >teknoloji</option>')
print ('<option value="vergi" >vergi</option>')
print ('<option value="sigorta" >sigorta</option>')
print ('<option value="arac bakim/onarim" >arac bakim/onarim</option>')
print ('<option value="ev bakim/onarim" >ev bakim/onarim</option>')

print ('</select>')
print('<br>Aciklama : <br><input type="text" name="aciklama" size="50" value="...">')


print('	<br><input type="submit" name="ekle" value="Ekle" style="color: #FFF; font-weight: bold;font-size: 200%; text-transform: uppercase; background-color: #900;">')



print ("</fieldset>")

print ('</form>')

print ("<hr>")

###################SON BİR AY TABLOSU##############################3

print('<table id="customers">')

print("<h2>SON BIR AYDAKI HARCAMALAR</h1>")

#sorgu="SELECT * FROM harcamalar WHERE date(tarihi)<date('2015-10-01')"
sorgu="SELECT * FROM harcamalar WHERE date(tarihi)>date('now','-30 days')"
cur.execute(sorgu)				
satirlar= cur.fetchall()

toplam="SELECT SUM(miktari) FROM harcamalar WHERE date(tarihi)>date('now','-30 days')"
cur.execute(toplam)
toplam_miktar=cur.fetchone()



tablo="<tr><th><b>ID</th><th><b>HARCANAN YER</th><th><b>MIKTAR</th>"+"<th><b>TARIHI</th><th><b>TURU</th><th><b>ACIKLAMA</th></tr>" #bu cok onemli!!!

for satir in satirlar:
	tablo=tablo+"<tr><td>"+str(satir[0])+"</td><td>"+str(satir[1])+"</td><td>"+str(satir[2])+"</td>"+"<td>"+str(satir[3])+"</td><td>"+str(satir[4])+"</td><td>"+str(satir[5])+"</td></tr>"
#return tablo	
print tablo,"<br>"

print ('<td>#</td><td style="color:blue;"><b>TOPLAM HARCAMA</td><td style="color:red;"><b>%s</b></td>') % toplam_miktar


###################BU AY TABLOSU##############################3

print('<table id="customers">')
print ("<hr>")
print("<h2>BU AYDAKI(%s) HARCAMALAR</h1>"%ay)

#sorgu="SELECT * FROM harcamalar WHERE date(tarihi)<date('2015-10-01')"
#SELECT * FROM table_name WHERE strftime('%m', date_column) = '04'
sorgu="SELECT * FROM harcamalar WHERE strftime('%m', tarihi) = '{0}'".format(str(ay))
#sorgu="SELECT * FROM harcamalar WHERE strftime('%m', tarihi) = '12'"
cur.execute(sorgu)				
satirlar= cur.fetchall()

toplam="SELECT SUM(miktari) FROM harcamalar WHERE strftime('%m', tarihi) = '{0}'".format(str(ay))
cur.execute(toplam)
toplam_miktar=cur.fetchone()



tablo="<tr><th><b>ID</th><th><b>HARCANAN YER</th><th><b>MIKTAR</th>"+"<th><b>TARIHI</th><th><b>TURU</th><th><b>ACIKLAMA</th></tr>" #bu cok onemli!!!

for satir in satirlar:
	tablo=tablo+"<tr><td>"+str(satir[0])+"</td><td>"+str(satir[1])+"</td><td>"+str(satir[2])+"</td>"+"<td>"+str(satir[3])+"</td><td>"+str(satir[4])+"</td><td>"+str(satir[5])+"</td></tr>"
#return tablo	
print tablo,"<br>"

print ('<td>#</td><td style="color:blue;"><b>TOPLAM HARCAMA</td><td style="color:red;"><b>%s</b></td>') % toplam_miktar


###################SON 1 AY TOP 10 TABLOSU##############################3

print('<table id="customers">')
print("<h2>SON BIR AY TOP 10</h1>")

#sorgu="SELECT * FROM harcamalar WHERE date(tarihi)<date('2015-10-01')"
#SELECT * FROM table_name WHERE strftime('%m', date_column) = '04'
sorgu="SELECT * FROM harcamalar WHERE date(tarihi)>date('now','-30 days') ORDER BY miktari DESC LIMIT 10" 
#sorgu="SELECT * FROM harcamalar WHERE strftime('%m', tarihi) = '12'"
cur.execute(sorgu)				
satirlar= cur.fetchall()

toplam="SELECT SUM(miktari) FROM harcamalar WHERE date(tarihi)>date('now','-30 days') ORDER BY miktari DESC LIMIT 10" 
cur.execute(toplam)
toplam_miktar=cur.fetchone()



tablo="<tr><th><b>ID</th><th><b>HARCANAN YER</th><th><b>MIKTAR</th>"+"<th><b>TARIHI</th><th><b>TURU</th><th><b>ACIKLAMA</th></tr>" #bu cok onemli!!!

harcanan_yerler=[]
miktarlar=[]
for satir in satirlar:
	tablo=tablo+"<tr><td>"+str(satir[0])+"</td><td>"+str(satir[1])+"</td><td>"+str(satir[2])+"</td>"+"<td>"+str(satir[3])+"</td><td>"+str(satir[4])+"</td><td>"+str(satir[5])+"</td></tr>"
	harcanan_yerler.append(str(satir[1]))
	miktarlar.append(int(satir[2]))
#return tablo	
print tablo,"<br>"

print ('<td>#</td><td style="color:blue;"><b>TOPLAM HARCAMA</td><td style="color:red;"><b>%s</b></td>') % toplam_miktar

######################grafik cizzitr###########################3
plt.bar(range(len(miktarlar)), miktarlar, align='center',color="red")
plt.xticks(range(len(harcanan_yerler)), harcanan_yerler)

#plt.show()
plt.savefig("top10harcama.jpg")
## grafigi bas########
print('<img src="top10harcama.jpg" style="width:50%;height:50%;" alt="" />')


###################SON 1 AY SEKTOREL ##############################3

print('<table id="customers">')
print("<hr>")	
print("<h2>SON BIR AY SEKTOREL TOP 5</h1>")

#sorgu="SELECT * FROM harcamalar WHERE date(tarihi)<date('2015-10-01')"
#SELECT * FROM table_name WHERE strftime('%m', date_column) = '04'
sorgu="SELECT turu,SUM(miktari) FROM harcamalar WHERE date(tarihi)>date('now','-30 days') GROUP BY turu ORDER BY SUM(miktari) DESC LIMIT 5" 
#sorgu="SELECT * FROM harcamalar WHERE strftime('%m', tarihi) = '12'"
cur.execute(sorgu)				
satirlar= cur.fetchall()


tablo="<tr><th>#</th><th><b>HARCANAN YER</th><th><b>TOPLAM MIKTAR</th></tr>" #bu cok onemli!!!
i=0
top_harcamalar=[]
top_harcamalar_miktarlar=[]
for satir in satirlar:
	i=i+1
	tablo=tablo+"<tr><td>"+str(i)+"</td><td>"+str(satir[0])+"</td><td>"+str(satir[1])+"</td></tr>"
	top_harcamalar.append(str(satir[0]))
	top_harcamalar_miktarlar.append(int(satir[1]))
#return tablo	
print tablo,"<br>"


######################grafik cizzitr###########################3

plt.figure()
#values = [3, 12, 5, 8] 
values=top_harcamalar_miktarlar

#labels = ['a', 'b', 'c', 'd'] 
labels=top_harcamalar

plt.pie(values, labels=labels, autopct='%.2f')
plt.show()
plt.savefig("top_sektor.jpg")

print('<img src="top_sektor.jpg" style="width:50%;height:50%;" alt="" />')

#########################





print('<hr>')
print ('</body></html>')