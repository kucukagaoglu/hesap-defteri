#!/usr/bin/python


import cgi, cgitb, os, time, sqlite3

## dd/mm/yyyy format
tarih=time.strftime("%d/%m/%Y")

baglanti=sqlite3.connect("/var/www/test/hesap.db")
cur=baglanti.cursor()

form=cgi.FieldStorage()
print ('Content-Type:text/html; charset=windows-1254\n')

cgitb.enable()

print('<html><title>Ekleme</title><body>')
print('<h1>Harcama Ekle!</h1>')


print('<table border="1">')


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

	cur.execute('''INSERT INTO harcamalar (adi,miktari,tarihi,turu,aciklama) VALUES ("%s","%d","%s","%s","%s")'''%(form['adi'].value,int(form['miktari'].value),form['tarihi'].value,form['dropdown'].value,form['aciklama'].value))
#	cur.execute('''INSERT INTO harcamalar ({},{},{},{})'''.format(form['adi'].value,int(form['miktari'].value),form['tarihi'].value,form['dropdown'].value))
	#cur.execute('''INSERT INTO harcamalar ({},{05d},{},{})'''.format("cagdas","55","12/12/2015","market"))
	baglanti.commit()


	print("</table>")
	print ('<td><b> Kayit basari ile eklendi!</b></td>')


print("</table>")

print ("<hr>")

print ('<form method="POST">')
print('<br>Harcama Yeri: <input type="text" name="adi">')
print('<br>Harcama Miktari: <input type="text" name="miktari">')
print('<br>Tarih: <input type="text" name="tarihi" value=%s>'%tarih)



print ('<br><select name="dropdown">')
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
print('<br>Aciklama : <input type="text" name="aciklama">')


print('	<br><input type="submit" name="ekle" value="Ekle">')
print ('</form>')

print ("<hr>")
print('<table border="1">')

print("<h2>SON YAPILAN HARCAMALAR</h1>")

sorgu="SELECT * FROM harcamalar"
cur.execute(sorgu)				
satirlar= cur.fetchall()

toplam="SELECT SUM(miktari) from harcamalar"
cur.execute(toplam)
toplam_miktar=cur.fetchone()



tablo="<tr><td><b>ID</td><td><b>HARCANAN YER</td><td><b>MIKTAR</td>"+"<td><b>TARIHI</td><td><b>TURU</td><td><b>ACIKLAMA</td></tr>" #bu cok onemli!!!

for satir in satirlar:
	tablo=tablo+"<tr><td>"+str(satir[0])+"</td><td>"+str(satir[1])+"</td><td>"+str(satir[2])+"</td>"+"<td>"+str(satir[3])+"</td><td>"+str(satir[4])+"</td><td>"+str(satir[5])+"</td></tr>"
#return tablo	
print tablo,"<br>"

print ('<td>#</td><td>TOPLAM HARCAMA</td><td><b>%s</b></td>') % toplam_miktar









print ('</body></html>')