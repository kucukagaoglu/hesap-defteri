#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb, os, time, sqlite3,datetime

## dd/mm/yyyy format
tarih=time.strftime("%Y-%m-%d")
simdi = datetime.datetime.now()
ay=simdi.month

baglanti=sqlite3.connect("/var/www/test/hesap.db")
cur=baglanti.cursor()

form=cgi.FieldStorage()
print ('Content-Type:text/html; charset=windows-1254\n')

cgitb.enable()

print('<html><title>Ekleme</title>')

print("""<style>

body {background-color:lightgrey}



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
		print ("</fieldset>")

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


print("</table>")

print ("<hr>")



print ('<form method="POST">')
print ("<fieldset>")
print("<legend><b> HARCAMA EKLE </legend>")
print('<br>Harcama Yeri:<br> <input type="text" name="adi">')
print('<br>Harcama Miktari: <br><input type="text" name="miktari">')
print('<br>Tarih(Yil-Ay-Gun): <br><input type="text" name="tarihi" value=%s>'%tarih)

print ('<br>Turu:<br><select name="dropdown">')
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


print('	<br><input type="submit" name="ekle" value="Ekle">')



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

print ('<td>#</td><td>TOPLAM HARCAMA</td><td><b>%s</b></td>') % toplam_miktar





###################BU AY TABLOSU##############################3

print('<table id="customers">')

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

print ('<td>#</td><td>TOPLAM HARCAMA</td><td><b>%s</b></td>') % toplam_miktar





print ('</body></html>')