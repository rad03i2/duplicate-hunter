# Duplicate Hunter

**Safe, local duplicate-file discovery for Windows, macOS, and Linux.**

Duplicate Hunter finds files that are truly byte-identical, estimates recoverable disk space, produces JSON reports, and can move redundant copies into a reversible quarantine folder. It never decides duplicates by filename alone and never auto-deletes files.

> Author: **Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — [@rad03i2](https://github.com/rad03i2)**

## Why it exists

Large download, photo, backup, and project folders often accumulate copies with different names. Deleting by name or size is unsafe. Duplicate Hunter narrows candidates by size and a fast prefix digest, then confirms duplicates with a full **SHA-256** hash.

## Features

- Exact duplicate detection using full SHA-256 verification.
- Efficient size → prefix hash → full hash pipeline to avoid hashing every file in full.
- Multiple files or directories in one scan; recursive scanning by default.
- Hidden files excluded by default; symbolic links skipped for safer traversal.
- `--min-size` filter for ignoring tiny files.
- Recoverable-space calculation per group and overall.
- JSON reports for automation and auditing.
- Safe quarantine workflow: preview by default, explicit `--apply` required.
- Keeps one copy from every group; moved copies get a manifest containing original/destination paths and hashes.
- Collision-safe quarantine filenames.
- No network access and no telemetry.

## Requirements & installation

Python **3.10+**.

```bash
git clone https://github.com/rad03i2/duplicate-hunter.git
cd duplicate-hunter
python -m pip install -e .
```

## Usage

Scan a directory:

```bash
duplicate-hunter ~/Downloads
```

Scan several locations and ignore files below 1 MiB:

```bash
duplicate-hunter ~/Downloads ~/Pictures --min-size 1048576
```

Create an audit report:

```bash
duplicate-hunter ~/Pictures --json duplicate-report.json
```

Preview which redundant copies would be quarantined:

```bash
duplicate-hunter ~/Pictures --quarantine ~/DuplicateQuarantine
```

After reviewing the printed plan, perform the moves:

```bash
duplicate-hunter ~/Pictures --quarantine ~/DuplicateQuarantine --apply
```

The quarantine directory receives `duplicate-hunter-manifest.json`. Duplicate Hunter **does not delete files**.

Useful switches:

```text
--no-recursive       only inspect the immediate directory
--include-hidden     include dot-files/dot-directories
--min-size BYTES     ignore smaller files
--json FILE          save a JSON report
--quarantine DIR     preview moving extra copies
--apply              perform the quarantine moves
```

## Safety & privacy

All hashing happens locally. Paths and hashes leave the computer only if you choose to send the generated report elsewhere. Symbolic links are ignored. Files that cannot be read are skipped. Hard-linked files are de-duplicated by filesystem identity during a scan so the same underlying file is not falsely counted twice.

Before using `--apply`, keep backups of important data and inspect the preview. Quarantine is deliberately safer than deletion, but external changes during a scan (another program renaming/modifying files) can still affect results.

## Project structure

```text
src/duplicate_hunter/core.py   scanning, hashing, grouping
src/duplicate_hunter/cli.py    CLI, JSON reporting, quarantine
tests/                         functional tests
.github/workflows/ci.yml       cross-platform lint/test matrix
```

## Testing

```bash
python -m pip install -e . pytest ruff
ruff check src tests
pytest
```

CI is configured for Python 3.10, 3.12, and 3.13 on Linux, Windows, and macOS.

## Limitations

- Equality is content-based; metadata such as filename and timestamps is intentionally irrelevant.
- SHA-256 confirmation requires reading candidate files, so very large duplicate sets can take time.
- The tool does not inspect inside archives or compare visually similar images.
- The quarantine manifest records moves; automatic restore is not currently implemented. Files can be restored manually using its source/destination paths.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**

---

# العربية

**Duplicate Hunter** أداة محلية وآمنة لاكتشاف الملفات المتطابقة فعليًا على ويندوز وماك ولينكس، وحساب المساحة التي يمكن استعادتها، وإنشاء تقارير JSON، ونقل النسخ الزائدة إلى مجلد عزل بدل حذفها.

## لماذا هذا المشروع؟

قد تحتوي مجلدات التنزيلات والصور والنسخ الاحتياطية على نسخ متعددة بأسماء مختلفة. الاعتماد على الاسم أو الحجم وحده غير آمن، لذلك تجمع الأداة الملفات حسب الحجم أولًا، ثم تستخدم بصمة أولية سريعة، وبعدها تؤكد التطابق الكامل باستخدام **SHA-256**.

## المزايا

- كشف التطابق الحقيقي بمقارنة المحتوى عبر SHA-256.
- فحص عدة ملفات أو مجلدات دفعة واحدة مع البحث داخل المجلدات الفرعية افتراضيًا.
- تجاهل الملفات المخفية والروابط الرمزية افتراضيًا لزيادة الأمان.
- تحديد حد أدنى للحجم لتجاهل الملفات الصغيرة.
- حساب المساحة القابلة للاستعادة لكل مجموعة وللفحص كاملًا.
- إخراج تقرير JSON مناسب للأرشفة والأتمتة.
- وضع عزل آمن: المعاينة هي الوضع الافتراضي، ولا يحدث النقل إلا مع `--apply`.
- الاحتفاظ بنسخة واحدة من كل مجموعة وإنشاء manifest بمسارات الملفات وبصماتها.
- لا اتصال بالشبكة ولا Telemetry.

## التثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/duplicate-hunter.git
cd duplicate-hunter
python -m pip install -e .
```

## الاستخدام

```bash
duplicate-hunter ~/Downloads
duplicate-hunter ~/Pictures --min-size 1048576
duplicate-hunter ~/Pictures --json duplicate-report.json
duplicate-hunter ~/Pictures --quarantine ~/DuplicateQuarantine
duplicate-hunter ~/Pictures --quarantine ~/DuplicateQuarantine --apply
```

الأمر قبل الأخير يعرض ما سيحدث فقط. إضافة `--apply` تنفذ النقل. البرنامج **لا يحذف النسخ تلقائيًا**.

## الخصوصية والأمان

كل الحسابات تتم محليًا. لا تُرفع أسماء الملفات أو البصمات لأي خدمة. الروابط الرمزية تُتجاهل، والملفات غير القابلة للقراءة يتم تجاوزها. قبل تنفيذ النقل على بيانات مهمة يُنصح بوجود نسخة احتياطية ومراجعة المعاينة.

## الاختبارات

```bash
python -m pip install -e . pytest ruff
ruff check src tests
pytest
```

تم إعداد GitHub Actions لاختبار المشروع على Linux وWindows وmacOS مع عدة إصدارات من Python.

## القيود

الأداة تبحث عن التطابق الكامل للمحتوى، وليست أداة للصور المتشابهة بصريًا ولا تفحص الملفات داخل الأرشيفات. قراءة الملفات الكبيرة اللازمة للتحقق الكامل قد تستغرق وقتًا. الاستعادة الآلية من مجلد العزل غير منفذة حاليًا، لكن ملف manifest يحتفظ بمسار المصدر والوجهة لتسهيل الاستعادة اليدوية.

## المساهمة والترخيص

راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة و[SECURITY.md](SECURITY.md) للإبلاغ الأمني. المشروع مرخص وفق MIT، والتفاصيل في [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**
