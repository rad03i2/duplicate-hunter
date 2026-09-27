# Contributing to Duplicate Hunter

Thank you for improving Duplicate Hunter. Changes should preserve the project's core principle: **file operations must remain explicit, reviewable, and safe by default**.

## Development setup

```bash
git clone https://github.com/rad03i2/duplicate-hunter.git
cd duplicate-hunter
python -m pip install -e . pytest ruff
```

## Before opening a pull request

Run:

```bash
ruff check src tests
pytest
```

For behavior changes:

- add or update tests;
- preserve preview-first quarantine behavior;
- do not introduce implicit deletion;
- keep duplicate confirmation content-based;
- document any new CLI behavior in the relevant README;
- update `CHANGELOG.md` when the change is user-visible.

## Pull request scope

Prefer focused pull requests with a clear reason for the change. A good description explains:

1. what changed;
2. why it changed;
3. how it was validated;
4. whether file-safety behavior is affected.

Do not commit secrets, credentials, personal file paths, virtual environments, generated reports containing private paths, or large real-world test fixtures.

## Documentation

The root `README.md` is the repository overview. Detailed language-specific guides live in:

- `README_EN.md`
- `README_AR.md`

Architecture claims must match the actual implementation. Planned features should not be described as current capabilities.

## Security-sensitive changes

Review [SECURITY.md](SECURITY.md) before changing traversal, hashing, destination selection, move behavior, report contents, or manifest handling.

---

<div dir="rtl">

## المساهمة

يرحب المشروع بالمساهمات المركزة التي تحافظ على مبدأه الأساسي: **أي تعامل مع ملفات المستخدم يجب أن يكون واضحًا وآمنًا افتراضيًا**.

قبل إرسال Pull Request شغّل:

</div>

```bash
ruff check src tests
pytest
```

<div dir="rtl">

أي تغيير في السلوك يجب أن يتضمن اختبارًا مناسبًا، وألا يضيف حذفًا تلقائيًا، وألا يحول وضع العزل إلى تنفيذ مباشر من دون `--apply`. كما يجب تحديث التوثيق إذا تغير سلوك واجهة سطر الأوامر.

</div>

Maintainer: **Radwan Abd alhady Ahmed — رضوان عبدالهادي — [@rad03i2](https://github.com/rad03i2)**
