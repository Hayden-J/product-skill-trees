"""셋업의 실제 파일 생성·기존 항목 보호 동작을 임시 폴더에서 확인한다."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "setup.sh"
FILES = {
    "AGENTS.md": "templates/AGENTS.template.md",
    "templates/AGENTS.template.md": "templates/AGENTS.template.md",
    "templates/PLAN.template.md": "templates/PLAN.template.md",
    "templates/COLLABORATION.template.md": "templates/COLLABORATION.template.md",
    "docs/PLAN.md": "templates/PLAN.template.md",
    "docs/COLLABORATION.md": "templates/COLLABORATION.template.md",
    "PROMPTS.md": "PROMPTS.md",
}


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill setup ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.task = self.base / "실제 과제 폴더"
        self.task.mkdir()

    def run_setup(self, *, explicit=False, cwd=None):
        return subprocess.run(
            ["bash", str(SCRIPT), *([str(self.task)] if explicit else [])],
            cwd=cwd or self.task, text=True, capture_output=True, timeout=10,
        )

    def test_first_install_from_working_directory(self):
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("복사 7, 건너뜀 0", result.stdout)
        for dest, source in FILES.items():
            self.assertEqual((self.task / dest).read_bytes(), (ROOT / source).read_bytes())
        self.assertFalse((self.task / ".agents").exists())
        self.assertNotIn("D-001 · 확정", (self.task / "docs/COLLABORATION.md").read_text())

    def test_explicit_destination_from_repo(self):
        result = self.run_setup(explicit=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.task / "PROMPTS.md").is_file())

    def test_repeat_preserves_content_and_metadata(self):
        self.assertEqual(self.run_setup().returncode, 0)
        for index, dest in enumerate(FILES):
            path = self.task / dest
            path.write_text(f"과제에서 수정한 내용 {index}\n")
            path.chmod(0o640)
            os.utime(path, (1_600_000_000, 1_600_000_000))
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("복사 0, 건너뜀 7", result.stdout)
        for index, dest in enumerate(FILES):
            path = self.task / dest
            self.assertEqual(path.read_text(), f"과제에서 수정한 내용 {index}\n")
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            self.assertEqual(path.stat().st_mtime, 1_600_000_000)

    def test_partial_install_preserves_existing_files(self):
        for dest in ["AGENTS.md", "docs/PLAN.md", "templates/PLAN.template.md"]:
            path = self.task / dest
            path.parent.mkdir(exist_ok=True)
            path.write_text("원본 유지\n")
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("복사 4, 건너뜀 3", result.stdout)
        self.assertEqual((self.task / "docs/PLAN.md").read_text(), "원본 유지\n")
        self.assertEqual((self.task / "docs/COLLABORATION.md").read_bytes(),
                         (ROOT / FILES["docs/COLLABORATION.md"]).read_bytes())

    def test_existing_symlinks_and_directory_are_preserved(self):
        outside = self.base / "outside.md"
        outside.write_text("링크 대상 원본\n")
        missing = self.base / "does-not-exist.md"
        (self.task / "AGENTS.md").symlink_to(outside)
        (self.task / "PROMPTS.md").symlink_to(missing)
        (self.task / "docs").mkdir()
        (self.task / "docs/PLAN.md").mkdir()
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("복사 4, 건너뜀 3", result.stdout)
        self.assertTrue((self.task / "AGENTS.md").is_symlink())
        self.assertTrue((self.task / "PROMPTS.md").is_symlink())
        self.assertTrue((self.task / "docs/PLAN.md").is_dir())
        self.assertEqual(outside.read_text(), "링크 대상 원본\n")
        self.assertFalse(missing.exists())

    def test_invalid_parent_stops_before_installing(self):
        for name in ["docs", "templates"]:
            for kind in ["file", "symlink", "dangling"]:
                with self.subTest(name=name, kind=kind):
                    dest = self.task / name
                    outside = self.base / f"outside-{name}-{kind}"
                    if kind == "file":
                        dest.write_text("원본 유지\n")
                    else:
                        if kind == "symlink":
                            outside.mkdir()
                        dest.symlink_to(outside)
                    result = self.run_setup()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse((self.task / "AGENTS.md").exists())
                    self.assertEqual(set(p.name for p in self.task.iterdir()), {name})
                    if outside.exists():
                        self.assertEqual(list(outside.iterdir()), [])
                    if kind == "file":
                        self.assertEqual(dest.read_text(), "원본 유지\n")
                    else:
                        self.assertTrue(dest.is_symlink())
                    dest.unlink()

    def test_repo_as_destination_is_rejected(self):
        result = self.run_setup(cwd=ROOT)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("스킬 저장소 자체에는 설치하지 않습니다", result.stderr)

    def test_missing_destination_and_help(self):
        missing = self.base / "missing"
        result = subprocess.run(["bash", str(SCRIPT), str(missing)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(missing.exists())
        result = subprocess.run(["bash", str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("사용법", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
