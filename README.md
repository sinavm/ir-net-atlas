# IR Net Atlas

رصدخانه زنده دسترسی سرویس‌های عمومی برای شرایط اینترنت ایران.

- پروب ساعتی از GitHub Actions (خارج از ایران)
- API: `docs/status.json`
- Badge: `docs/badge.svg`
- گزارش مردمی داخل ایران: `reports/iran.json`

این ریپو لینک فیلترشکن نیست. وضعیت سرویس‌ها را جدا از دید رانر جهانی و گزارش داخل ایران نگه می‌دارد.

## لینک‌ها

- ریپو: https://github.com/sinavm/ir-net-atlas
- صفحه: https://sinavm.github.io/ir-net-atlas/
- API: https://sinavm.github.io/ir-net-atlas/status.json
- Badge: https://sinavm.github.io/ir-net-atlas/badge.svg

## اجرای محلی

```bash
python3 probe.py
```

## گزارش از داخل ایران

به `reports/iran.json` اضافه کنید یا از ایشو قالب `iran-report` استفاده کنید.

```json
{
  "at": "2026-09-25T08:00:00Z",
  "isp": "mci",
  "city": "tehran",
  "target": "youtube",
  "ok": false,
  "note": "timeout after 10s"
}
```
