# AzizDownloader

این پروژه یک دانلودر ویدیو از یوتیوب است که با استفاده از پایتون و کتابخانه‌های `yt-dlp` و `tkinter` ساخته شده است. شما می‌توانید با وارد کردن لینک ویدیو، فرمت‌های مختلف ویدیو و صدا را انتخاب کرده و آنها را دانلود کنید.

## نصب و راه‌اندازی

1. **کلون کردن پروژه**:
   ابتدا پروژه را از GitHub کلون کنید:
   
   ```bash
   git clone https://github.com/Azizmaghsuomi/YoutubeDownlader.git
   cd YoutubeDownlader
  ## ایجاد محیط مجازی

برای ایجاد محیط مجازی پایتون دستور زیر را اجرا کنید:

``python -m venv .venv ``
## فعال‌سازی محیط مجازی 

## در ویندوز: 
`` .\.venv\Scripts\activate``
## در مک یا لینوکس:
``source .venv/bin/activate``

  ##  نصب وابستگی‌ها

برای نصب پکیج‌های مورد نیاز، دستور زیر را اجرا کنید:

``pip install -r requirements.txt``
  ## اجرای پروژه

پس از نصب وابستگی‌ها، برای اجرای برنامه دستور زیر را وارد کنید:

``python yt_downloader.py``
## توضیحات
این پروژه به شما امکان می‌دهد تا ویدیوها و فایل‌های صوتی یوتیوب را با استفاده از فرمت‌های مختلف دانلود کنید. شما می‌توانید فرمت‌های مختلف ویدیو را مشاهده کرده و انتخاب کنید، سپس ویدیو را در پوشه‌ای که انتخاب کرده‌اید ذخیره کنید.

استفاده از فایل کوکی
برای دانلود ویدیوها از یوتیوب، نیاز به فایل کوکی دارید. این فایل را از مرورگر خود استخراج کرده و مسیر آن را در پروژه قرار دهید. مسیر پیش‌فرض فایل کوکی در کد C:\Users\myhp2\Downloads\www.youtube.com_cookies است. می‌توانید این مسیر را مطابق با سیستم خود تغییر دهید.

ویژگی‌ها
نمایش فرمت‌های مختلف ویدیو و صدا
امکان دانلود ویدیو با فرمت ترکیبی ویدیو و صدا
نمایش پیشرفت دانلود در کنسول
رابط گرافیکی مدرن با استفاده از ttkbootstrap و tkinter
انتخاب پوشه برای ذخیره فایل‌های دانلود شده
