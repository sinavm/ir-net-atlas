<div align="center">

# SVM و SiNAVM

<p>
  <a href="https://github.com/sinavm/ir-net-atlas/stargazers"><img src="https://img.shields.io/github/stars/sinavm/ir-net-atlas?style=for-the-badge&logo=github&color=f59e0b&label=Stars" alt="ستاره‌های مخزن"></a>
  <a href="https://github.com/sinavm/ir-net-atlas/blob/main/LICENSE"><img src="https://img.shields.io/github/license/sinavm/ir-net-atlas?style=for-the-badge&color=10b981" alt="مجوز MIT"></a>
  <a href="https://github.com/sinavm/ir-net-atlas/commits/main"><img src="https://img.shields.io/github/last-commit/sinavm/ir-net-atlas?style=for-the-badge&color=64748b" alt="آخرین به‌روزرسانی"></a>
  <a href="https://sinavm.github.io/ir-net-atlas/"><img src="https://img.shields.io/badge/Live-Dashboard-0891b2?style=for-the-badge&logo=githubpages&logoColor=white" alt="داشبورد زنده"></a>
</p>

<h2>SiNAVM | Iran Internet Reachability Observatory</h2>

<a href="https://github.com/sinavm/ir-net-atlas"><img src="https://img.shields.io/badge/Star-IR%20Net%20Atlas-f59e0b?style=for-the-badge&logo=github&logoColor=white" alt="Star IR Net Atlas on GitHub"></a><br>
<a href="https://sinavm.github.io/ir-net-atlas/"><img src="https://img.shields.io/badge/Open-Live%20Atlas-0891b2?style=for-the-badge&logo=githubpages&logoColor=white" alt="Open Live Atlas"></a><br>
<a href="https://t.me/sinavm"><img src="https://img.shields.io/badge/Join-SVM%20on%20Telegram-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Join SVM on Telegram"></a>

<p>
  <a href="https://sinavm.github.io/ir-net-atlas/"><img src="https://raw.githubusercontent.com/sinavm/ir-net-atlas/main/docs/badge.svg" alt="وضعیت فعلی اطلس"></a>
</p>

</div>

---

**IR Net Atlas** رصدخانه‌ای عمومی برای سنجش دسترسی‌پذیری وب‌سایت‌ها و سرویس‌های اینترنتی مرتبط با ایران است.

## داده‌های زنده

- **۲۳ مقصد داخلی** شامل وب‌سایت‌ها، APIها، سرویس‌های پرداخت، اپراتورها و پیام‌رسان‌ها
- **۲۶ مقصد بین‌المللی** برای بررسی از طریق مرورگر کاربر
- **پایش بیرونی** با GitHub Actions و ثبت وضعیت HTTP، زمان پاسخ و زمان DNS
- **داده‌های داخل ایران** با اولویت ArvanCloud Radar و استفاده از OONI در صورت در دسترس بودن
- **تاریخچه و نمودار** برای مشاهده تغییرات دسترسی و زمان پاسخ

## منابع داده

| منبع | کاربرد |
|:--|:--|
| [وضعیت فعلی](https://sinavm.github.io/ir-net-atlas/status.json) | آخرین نتیجه پروب بیرونی و وضعیت هر مقصد |
| [تاریخچه](https://sinavm.github.io/ir-net-atlas/history.json) | snapshotهای ثبت‌شده برای بررسی روند |
| [مشاهدات داخل ایران](https://sinavm.github.io/ir-net-atlas/inside.json) | داده‌های دریافت‌شده از Radar یا OONI |
| [فهرست مقصدها](https://sinavm.github.io/ir-net-atlas/targets.json) | مقصدهای بین‌المللی مورد استفاده در بررسی مرورگر |
| [نشان وضعیت](https://sinavm.github.io/ir-net-atlas/badge.svg) | نشان SVG قابل استفاده در پروژه‌های دیگر |

## روش اندازه‌گیری

پروب بیرونی به‌صورت زمان‌بندی‌شده اجرا می‌شود و نتیجه هر مقصد را همراه با کد HTTP، زمان پاسخ، زمان DNS و سطح کیفیت ثبت می‌کند.

| سطح | زمان پاسخ |
|:--|--:|
| Fast | کمتر از ۲۰۰ میلی‌ثانیه |
| OK | از ۲۰۰ تا ۷۹۹ میلی‌ثانیه |
| Slow | ۸۰۰ میلی‌ثانیه یا بیشتر |
| Down | درخواست ناموفق یا مقصد غیرقابل دسترس |

**نکته مهم:** پروب GitHub Actions خارج از ایران اجرا می‌شود و به‌تنهایی وضعیت دسترسی کاربران داخل ایران را نشان نمی‌دهد. داده‌های بیرونی، مشاهدات داخل ایران و بررسی مرورگر منابع اندازه‌گیری جداگانه‌اند.

## به‌روزرسانی

گردآوری داده‌ها طبق زمان‌بندی ساعتی و یک اجرای تکمیلی هر سه ساعت انجام می‌شود. اجرای دستی نیز از [GitHub Actions](https://github.com/sinavm/ir-net-atlas/actions/workflows/probe.yml) در دسترس است.

## مشارکت

برای افزودن مقصد یا گزارش اختلال، [راهنمای مشارکت](CONTRIBUTING.md) و [فرم گزارش از داخل ایران](https://github.com/sinavm/ir-net-atlas/issues/new?template=iran-report.yml) را ببینید.

## مجوز

[MIT License](LICENSE)

---

<div align="center">

**Built by [SiNAVM](https://github.com/sinavm)**

[Live Atlas](https://sinavm.github.io/ir-net-atlas/) · [GitHub](https://github.com/sinavm/ir-net-atlas) · [Telegram](https://t.me/sinavm)

</div>
