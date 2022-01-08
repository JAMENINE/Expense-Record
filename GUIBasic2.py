# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by JAMENINE')
GUI.geometry('500x500+500+50')


###################MENU####################
menubar = Menu(GUI)
GUI.config(menu=menubar)


#################Background########################
bg = PhotoImage(file='iconmoney.png')
gui_background = Label(GUI,image=bg)
gui_background.place(x=0,y=0,relwidth=1,relheight=1)

# Help
def About():
	messagebox.showinfo('About','สวัสดีครับ โปรเเกรมนี้คือโปรเเกรมบันทึดข้อมูล\ndevelop by JAMENINE ')

helpmenu = Menu(menubar)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)




###########################################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

icon_t1 = PhotoImage(file='t1_expense.png')
icon_t2 = PhotoImage(file='t2_expenselist.png')


Tab.add(T1, text=f'{"Add Expense": ^50s}', image=icon_t1,compound='top')
Tab.add(T2, text=f'{"Expense List": ^50s}', image=icon_t2,compound='top')

F1 = Frame(T1)
F1.pack()

days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัสบดี',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(event=None):
	expense = v_expense.get()
	price = v_price.get()
	quantity = v_quantity.get()

	if expense == '':
		print('No Data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกราคา')
		return
	elif quantity == '':
		quantity = 1
		


	try:
		total = int(price) * int(quantity)
		today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
		print(today)
		dt = datetime.now().strftime('%Y-%m-%d')
		dt = days[today] + '-' + dt
		with open('savedata.csv','a',encoding='utf-8',newline='') as f:
			# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
			# newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้างฟังชั่นสำหรับเขียนข้อมูล
			data = [dt,expense,price,quantity,total]
			fw.writerow(data)

		# ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
		E1.focus()
		update_table()

	except Exception as e:
		print('Error:,e')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')
# ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,16) 

main_icon = PhotoImage(file='iconmoney.png')

Mainicon = Label(F1,image=main_icon)
Mainicon.pack()
	   
#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-------------------

#------text2--------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#-------------------

#------text3--------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-------------------

icon_b1 = PhotoImage(file='b_save.png')

B2 = ttk.Button(F1,text=f'{"Save":>{10}}',command=Save,image=icon_b1,compound='left')
B2.pack(ipadx=38,ipady=8,pady=8)

####################TAB2#######################

rs = []

def read_csv():
	with open('savedata.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data
		

#Table
L = ttk.Label(T2,text='ตารางเเสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['วันที่ทำรายการ','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=15)
resulttable.pack()

for i in range(len(header)):
	resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [100,120,70,70,70]
for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)

def update_table():
	resulttable.delete(*resulttable.get_children())
	data = read_csv()
	for d in data:
		resulttable.insert('',0,value=d)


#update_record()
update_table()
print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
