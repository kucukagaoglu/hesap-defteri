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
		print ('<td><b> Harcama Adi:</b></td><td>%s</td></tr>' % form['adi'].value)	
	if form.getvalue('miktari'):
		print ('<td><b> Harcama Miktari:</b></td><td>%s TL</td></tr>' % form['miktari'].value)
	if form.getvalue('tarihi'):
		print ('<td><b> Harcama Tarihi:</b></td><td>%s</td></tr>' % form['tarihi'].value)
	if form.getvalue('dropdown'):
		print ('<td><b> Harcama Turu:</b></td><td>%s</td></tr>' % form['dropdown'].value)

	cur.execute('''INSERT INTO harcamalar (adi,miktari,tarihi,turu) VALUES ("%s","%d","%s","%s")'''%(form['adi'].value,int(form['miktari'].value),form['tarihi'].value,form['dropdown'].value))
#	cur.execute('''INSERT INTO harcamalar ({},{},{},{})'''.format(form['adi'].value,int(form['miktari'].value),form['tarihi'].value,form['dropdown'].value))
	#cur.execute('''INSERT INTO harcamalar ({},{05d},{},{})'''.format("cagdas","55","12/12/2015","market"))
	baglanti.commit()


	print("</table>")
	print ('<td><b> Kayit basari ile eklendi!</b></td>')


print("</table>")












print ('<form method="POST">')
print('<br>Harcama Adi: <input type="text" name="adi">')
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


print('	<input type="submit" name="ekle" value="Ekle">')
print ('</form>')
print ('</body></html>')
