"""셋업의 실제 파일 생성·기존 항목 보호 동작을 임시 폴더에서 확인한다."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "setup.sh"
FILES = {
    "AGENTS.md": "templates/AGENTS.template.md",
    "templates/AGENTS.template.md": "templates/AGENTS.template.md",
    "templates/PLAN.template.md": "templates/PLAN.template.md",
    "templates/WORKLOG.template.md": "templates/WORKLOG.template.md",
    "docs/PLAN.md": "templates/PLAN.template.md",
    "docs/WORKLOG.md": "templates/WORKLOG.template.md",
    "PROMPTS.md": "PROMPTS.md",
}
SKILLS = (
    "discovery-interview", "define-problem", "clarify-requirements",
    "evaluate-solutions", "verify-work-results",
)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill setup ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.task = self.base / "실제 과제 폴더"
        self.task.mkdir()

    def run_setup(self, *, explicit=False, cwd=None, script=SCRIPT):
        return subprocess.run(
            ["bash", str(script), *([str(self.task)] if explicit else [])],
            cwd=cwd or self.task, text=True, capture_output=True, timeout=10,
        )

    def test_first_install_from_working_directory(self):
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("복사 7, 건너뜀 0", result.stdout)
        for dest, source in FILES.items():
            self.assertEqual((self.task / dest).read_bytes(), (ROOT / source).read_bytes())
        self.assertIn("스킬 설치 5, 건너뜀 0", result.stdout)
        installed = self.task / ".agents/skills"
        self.assertEqual({p.name for p in installed.iterdir()}, set(SKILLS))
        for name in SKILLS:
            source = ROOT / "skills" / name
            expected = {p.relative_to(source) for p in source.rglob("*") if p.is_file()}
            actual = {p.relative_to(installed / name) for p in (installed / name).rglob("*")
                      if p.is_file()}
            self.assertEqual(actual, expected | {Path("LICENSE")})
            for relative in expected:
                self.assertEqual((installed / name / relative).read_bytes(),
                                 (source / relative).read_bytes())
            self.assertEqual((installed / name / "LICENSE").read_bytes(),
                             (ROOT / "LICENSE").read_bytes())
        rows = [line for line in (self.task / "docs/WORKLOG.md").read_text().splitlines()
                if line.startswith("|")]
        self.assertEqual(rows, ["| 시각 | 상대(담당자/Codex/나) | 내용 | 결정 | 근거 |",
                                "| --- | --- | --- | --- | --- |"])

    def test_distribution_worklog_has_no_history(self):
        template = ROOT / "templates/WORKLOG.template.md"
        self.assertEqual((ROOT / "docs/WORKLOG.md").read_bytes(), template.read_bytes())
        self.assertEqual(len([line for line in template.read_text().splitlines()
                              if line.startswith("|")]), 2)

    def test_explicit_destination_from_repo(self):
        result = self.run_setup(explicit=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.task / "PROMPTS.md").is_file())

    def test_repeat_preserves_content_and_metadata(self):
        self.assertEqual(self.run_setup().returncode, 0)
        paths = list(FILES) + [f".agents/skills/{name}/SKILL.md" for name in SKILLS]
        for index, dest in enumerate(paths):
            path = self.task / dest
            path.write_text(f"과제에서 수정한 내용 {index}\n")
            path.chmod(0o640)
            os.utime(path, (1_600_000_000, 1_600_000_000))
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("복사 0, 건너뜀 7", result.stdout)
        self.assertIn("스킬 설치 0, 건너뜀 5", result.stdout)
        for index, dest in enumerate(paths):
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
        self.assertEqual((self.task / "docs/WORKLOG.md").read_bytes(),
                         (ROOT / FILES["docs/WORKLOG.md"]).read_bytes())

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
        for name in ["docs", "templates", ".agents", ".agents/skills"]:
            for kind in ["file", "symlink", "dangling"]:
                with self.subTest(name=name, kind=kind):
                    dest = self.task / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    outside = self.base / f"outside-{name.replace('/', '-')}-{kind}"
                    if kind == "file":
                        dest.write_text("원본 유지\n")
                    else:
                        if kind == "symlink":
                            outside.mkdir()
                        dest.symlink_to(outside)
                    before = set(self.task.rglob("*"))
                    result = self.run_setup()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse((self.task / "AGENTS.md").exists())
                    self.assertEqual(set(self.task.rglob("*")), before)
                    if outside.exists():
                        self.assertEqual(list(outside.iterdir()), [])
                    if kind == "file":
                        self.assertEqual(dest.read_text(), "원본 유지\n")
                    else:
                        self.assertTrue(dest.is_symlink())
                    dest.unlink()

    def test_installed_skill_links_are_self_contained(self):
        self.assertEqual(self.run_setup().returncode, 0)
        for name in SKILLS:
            bundle = (self.task / ".agents/skills" / name).resolve()
            for doc in bundle.rglob("*.md"):
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
                    if "://" in target or target.startswith("#"):
                        continue
                    linked = (doc.parent / target.split("#")[0]).resolve()
                    self.assertTrue(linked.is_relative_to(bundle), (doc, target))
                    self.assertTrue(linked.is_file(), (doc, target))

    def test_existing_partial_skill_is_not_mixed_with_new_version(self):
        skill = self.task / ".agents/skills/discovery-interview"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("기존 스킬 본문\n")
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("스킬 설치 4, 건너뜀 1", result.stdout)
        self.assertEqual((skill / "SKILL.md").read_text(), "기존 스킬 본문\n")
        self.assertEqual({p.name for p in skill.iterdir()}, {"SKILL.md"})

    def test_existing_skill_files_and_links_are_preserved(self):
        installed = self.task / ".agents/skills"
        installed.mkdir(parents=True)
        outside = self.base / "existing skill"
        outside.mkdir()
        (outside / "SKILL.md").write_text("외부 원본\n")
        missing = self.base / "missing skill"
        (installed / SKILLS[0]).symlink_to(outside)
        (installed / SKILLS[1]).symlink_to(missing)
        (installed / SKILLS[2]).write_text("같은 이름의 파일\n")
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("스킬 설치 2, 건너뜀 3", result.stdout)
        self.assertTrue((installed / SKILLS[0]).is_symlink())
        self.assertTrue((installed / SKILLS[1]).is_symlink())
        self.assertEqual((installed / SKILLS[2]).read_text(), "같은 이름의 파일\n")
        self.assertEqual({p.name for p in outside.iterdir()}, {"SKILL.md"})
        self.assertEqual((outside / "SKILL.md").read_text(), "외부 원본\n")
        self.assertFalse(missing.exists())

    def make_source_copy(self):
        source = self.base / "설치 원본"
        source.mkdir(exist_ok=True)
        for filename in ["setup.sh", "PROMPTS.md", "LICENSE"]:
            shutil.copy2(ROOT / filename, source / filename)
        for dirname in ["templates", "skills"]:
            shutil.copytree(ROOT / dirname, source / dirname, dirs_exist_ok=True)
        return source

    def test_missing_required_source_stops_before_installing(self):
        for relative in ["templates/PLAN.template.md", "LICENSE",
                         "skills/define-problem/SKILL.md",
                         "skills/verify-work-results/assets/output-template.md"]:
            with self.subTest(relative=relative):
                source = self.make_source_copy()
                (source / relative).unlink()
                result = self.run_setup(script=source / "setup.sh")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list(self.task.iterdir()), [])

    def test_source_skill_symlink_stops_before_installing(self):
        source = self.make_source_copy()
        outside = self.base / "linked reference.md"
        outside.write_text("외부 자료\n")
        (source / "skills/define-problem/linked.md").symlink_to(outside)
        result = self.run_setup(script=source / "setup.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.task.iterdir()), [])
        self.assertEqual(outside.read_text(), "외부 자료\n")

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
