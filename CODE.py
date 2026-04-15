import json
import os
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, simpledialog

# -----------------------------
# JSON file setup
# -----------------------------
DATA_FILE = "grades.json"

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
else:
    data = {}

# -----------------------------
# LOGIC FUNCTIONS
# -----------------------------
def convert_to_GWA(gwa):
    if 96.00 <= gwa <= 100.00: return "1.00"
    elif 90.00 <= gwa:         return "1.25"
    elif 84.00 <= gwa:         return "1.50"
    elif 78.00 <= gwa:         return "1.75"
    elif 72.00 <= gwa:         return "2.00"
    elif 66.00 <= gwa:         return "2.25"
    elif 60.00 <= gwa:         return "2.50"
    elif 55.00 <= gwa:         return "2.75"
    else:                      return "3.00 or below"

def cap_gwa(gwa):
    return min(gwa, 100.0)

def apply_carry(previous_gwa, current_gwa):
    return min((previous_gwa * (1/3)) + (current_gwa * (2/3)), 100.0)

def get_previous_quarter_grade(user_id, quarter):
    order = ["Q1", "Q2", "Q3", "Q4"]
    if user_id not in data:      return None
    if quarter not in order:     return None
    idx = order.index(quarter)
    if idx == 0:                 return None
    prev_quarter = order[idx - 1]
    if "quarters" in data[user_id] and prev_quarter in data[user_id]["quarters"]:
        return data[user_id]["quarters"][prev_quarter]["overall_gwa"]
    return None

def save_grade_json(user_id, user_name, grade_level, section, quarter, subjects, overall_gwa):
    if user_id not in data:
        data[user_id] = {
            "name": user_name, "grade_level": grade_level,
            "section": section, "quarters": {}
        }
    data[user_id]["quarters"][quarter] = {
        "subjects": subjects,
        "overall_gwa": overall_gwa
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_required_score(current_grade, desired_grade, weight_remaining):
    if weight_remaining <= 0:
        return "No remaining weight to compute."
    needed = (desired_grade - current_grade) / (weight_remaining / 100)
    if needed > 100:  return "Unfortunately, it's not possible to reach your desired grade."
    elif needed < 0:  return "You have already surpassed your desired grade!"
    else:             return f"You need {needed:.2f}% on the remaining assessments."

GWA_TABLE = [
    ("96-100",   "1.00"), ("90-95",  "1.25"), ("84-89", "1.50"),
    ("78-83",    "1.75"), ("72-77",  "2.00"), ("66-71", "2.25"),
    ("60-65",    "2.50"), ("55-59",  "2.75"), ("Below 55", "3.00 or below"),
]

# -----------------------------
# STYLE CONSTANTS
# -----------------------------
BG_MAIN    = "#ffd6e7"
BG_FRAME   = "white"
FG_TITLE   = "#ff4da6"
BTN_BG     = "pink"
BTN_DEL    = "#ffb3cc"
FONT_TITLE = ("Arial", 14, "bold")
FONT_BOLD  = ("Arial", 10, "bold")
FONT_BTN   = ("Arial", 10, "bold")
FONT_MONO  = ("Courier", 9)

# -----------------------------
# SCROLLABLE FRAME HELPER
# -----------------------------
class ScrollableFrame(tk.Frame):
    """A Frame with a vertical scrollbar; inner content expands with the widget."""

    def __init__(self, parent, bg=BG_FRAME, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.vbar   = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner  = tk.Frame(self.canvas, bg=bg)

        self.inner.bind("<Configure>",  self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self._win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vbar.set)

        self.canvas.pack(side="left",  fill="both", expand=True)
        self.vbar.pack  (side="right", fill="y")

        # Mouse-wheel scrolling
        self.canvas.bind("<Enter>", self._bind_wheel)
        self.canvas.bind("<Leave>", self._unbind_wheel)

    def _on_inner_configure(self, _e=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self._win_id, width=event.width)

    def _bind_wheel(self, _e):
        self.canvas.bind_all("<MouseWheel>", self._scroll)
        self.canvas.bind_all("<Button-4>",   self._scroll)
        self.canvas.bind_all("<Button-5>",   self._scroll)

    def _unbind_wheel(self, _e):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _scroll(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# -----------------------------
# SUBJECT INPUT DIALOGUE
# -----------------------------
class SubjectDialog(tk.Toplevel):
    """Resizable modal dialog to enter one subject's grade information."""

    def __init__(self, parent, subject_name):
        super().__init__(parent)
        self.title(f"Subject: {subject_name}")
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)
        self.minsize(440, 480)
        self.grab_set()

        self.result_gwa   = None
        self.subject_name = subject_name

        sf = ScrollableFrame(self, bg=BG_FRAME)
        sf.pack(fill="both", expand=True, padx=8, pady=8)
        self.f = sf.inner
        
        # Allow grade entry columns to stretch
        self.f.columnconfigure(2, weight=1)
        self.f.columnconfigure(3, weight=1)

        self._build_form()
        self.geometry("480x660")

    def _build_form(self):
        f   = self.f
        pad = {"padx": 10, "pady": 4}

        tk.Label(f, text=f"🌸 {self.subject_name}", bg=BG_FRAME,
                 fg=FG_TITLE, font=FONT_TITLE).grid(
            row=0, column=0, columnspan=4, pady=10)

        def sec(text, row):
            tk.Label(f, text=text, bg=BG_FRAME, font=FONT_BOLD).grid(
                row=row, column=0, columnspan=4, sticky="w", **pad)

        def wt_entry(row, col, default="0"):
            tk.Label(f, text="Weight (%):", bg=BG_FRAME).grid(
                row=row, column=col, sticky="e", **pad)
            e = tk.Entry(f, width=6)
            e.insert(0, default)
            e.grid(row=row, column=col+1, sticky="w", **pad)
            return e

        def grade_row(row):
            tk.Label(f, text="Grades (comma-sep):", bg=BG_FRAME).grid(
                row=row, column=0, columnspan=2, sticky="e", **pad)
            e = tk.Entry(f)
            e.grid(row=row, column=2, columnspan=2, sticky="ew", **pad)
            return e

        # Formative
        sec("Formative Assessments (max 10)", 1)
        tk.Label(f, text="Count (0–10):", bg=BG_FRAME).grid(row=2, column=0, sticky="e", **pad)
        self.fa_count  = tk.Spinbox(f, from_=0, to=10, width=5)
        self.fa_count.grid(row=2, column=1, sticky="w", **pad)
        self.fa_weight = wt_entry(2, 2)
        self.fa_grades = grade_row(3)

        # Alternative
        sec("Alternative Assessments (max 7)", 4)
        tk.Label(f, text="Count (0–7):", bg=BG_FRAME).grid(row=5, column=0, sticky="e", **pad)
        self.aa_count  = tk.Spinbox(f, from_=0, to=7, width=5)
        self.aa_count.grid(row=5, column=1, sticky="w", **pad)
        self.aa_weight = wt_entry(5, 2)
        self.aa_grades = grade_row(6)

        # Long Test
        sec("Long Test (optional)", 7)
        self.lt_take = tk.IntVar(value=0)
        tk.Checkbutton(f, text="Took Long Test", variable=self.lt_take,
                       bg=BG_FRAME).grid(row=8, column=0, columnspan=2, sticky="w", **pad)
        self.lt_weight = wt_entry(8, 2)
        self.lt_grades = grade_row(9)

        # Practical Exam
        sec("Practical Exam (optional)", 10)
        self.pr_take = tk.IntVar(value=0)
        tk.Checkbutton(f, text="Took Practical Exam", variable=self.pr_take,
                       bg=BG_FRAME).grid(row=11, column=0, columnspan=2, sticky="w", **pad)
        self.pr_weight = wt_entry(11, 2)
        self.pr_grades = grade_row(12)

        # Midterm
        sec("Midterm (optional)", 13)
        self.mt_take = tk.IntVar(value=0)
        tk.Checkbutton(f, text="Took Midterm", variable=self.mt_take,
                       bg=BG_FRAME).grid(row=14, column=0, columnspan=2, sticky="w", **pad)
        self.mt_weight = wt_entry(14, 2)
        self.mt_grades = grade_row(15)

        # Final Exam
        sec("Final Exam (optional)", 16)
        self.fe_take = tk.IntVar(value=0)
        tk.Checkbutton(f, text="Took Final Exam", variable=self.fe_take,
                       bg=BG_FRAME).grid(row=17, column=0, columnspan=2, sticky="w", **pad)
        self.fe_weight = wt_entry(17, 2)
        tk.Label(f, text="Score (0–100):", bg=BG_FRAME).grid(
            row=18, column=0, columnspan=2, sticky="e", **pad)
        self.fe_grade = tk.Entry(f, width=10)
        self.fe_grade.insert(0, "0")
        self.fe_grade.grid(row=18, column=2, columnspan=2, sticky="w", **pad)

        # Bonus
        tk.Label(f, text="Bonus Points (0–5):", bg=BG_FRAME, font=FONT_BOLD).grid(
            row=19, column=0, columnspan=2, sticky="e", **pad)
        self.bonus = tk.Entry(f, width=6)
        self.bonus.insert(0, "0")
        self.bonus.grid(row=19, column=2, columnspan=2, sticky="w", **pad)

        # Submit
        tk.Button(f, text="Calculate Subject GWA", bg=BTN_BG, font=FONT_BTN,
                  command=self._submit).grid(
            row=20, column=0, columnspan=4, pady=12, sticky="ew", padx=10)

        self.result_lbl = tk.Label(f, text="", bg=BG_FRAME,
                                   fg=FG_TITLE, font=("Arial", 11, "bold"))
        self.result_lbl.grid(row=21, column=0, columnspan=4, pady=6)

    def _parse_grades(self, widget, label):
        raw = widget.get().strip()
        if not raw:
            return []
        try:
            vals = [float(x) for x in raw.split(",")]
            for v in vals:
                if not (0 <= v <= 100):
                    raise ValueError
            return vals
        except ValueError:
            raise ValueError(
                f"Invalid grades for {label}. Enter numbers 0–100 separated by commas.")

    def _parse_weight(self, widget, label):
        try:
            w = float(widget.get())
            if not (0 <= w <= 100):
                raise ValueError
            return w
        except ValueError:
            raise ValueError(f"Invalid weight for {label}.")

    def _calc_section(self, grades, weight):
        if not grades or weight == 0:
            return 0.0
        return (sum(grades) / len(grades)) * (weight / 100)

    def _submit(self):
        try:
            tc = tw = 0.0          # total_contribution, total_weight

            fa_n = int(self.fa_count.get())
            if fa_n > 0:
                fa_w  = self._parse_weight(self.fa_weight, "Formative")
                fa_gs = self._parse_grades(self.fa_grades, "Formative")
                if len(fa_gs) != fa_n:
                    raise ValueError(f"Expected {fa_n} Formative grade(s), got {len(fa_gs)}.")
                tc += self._calc_section(fa_gs, fa_w); tw += fa_w

            aa_n = int(self.aa_count.get())
            if aa_n > 0:
                aa_w  = self._parse_weight(self.aa_weight, "Alternative")
                aa_gs = self._parse_grades(self.aa_grades, "Alternative")
                if len(aa_gs) != aa_n:
                    raise ValueError(f"Expected {aa_n} Alternative grade(s), got {len(aa_gs)}.")
                tc += self._calc_section(aa_gs, aa_w); tw += aa_w

            if self.lt_take.get():
                lt_w  = self._parse_weight(self.lt_weight, "Long Test")
                lt_gs = self._parse_grades(self.lt_grades, "Long Test")
                if not lt_gs:
                    raise ValueError("Enter at least one Long Test grade.")
                tc += self._calc_section(lt_gs, lt_w); tw += lt_w

            if self.pr_take.get():
                pr_w  = self._parse_weight(self.pr_weight, "Practical Exam")
                pr_gs = self._parse_grades(self.pr_grades, "Practical Exam")
                if not pr_gs:
                    raise ValueError("Enter at least one Practical Exam grade.")
                tc += self._calc_section(pr_gs, pr_w); tw += pr_w

            if self.mt_take.get():
                mt_w  = self._parse_weight(self.mt_weight, "Midterm")
                mt_gs = self._parse_grades(self.mt_grades, "Midterm")
                if not mt_gs:
                    raise ValueError("Enter at least one Midterm grade.")
                tc += self._calc_section(mt_gs, mt_w); tw += mt_w

            if self.fe_take.get():
                fe_w = self._parse_weight(self.fe_weight, "Final Exam")
                fe_g = float(self.fe_grade.get())
                if not (0 <= fe_g <= 100):
                    raise ValueError("Final exam score must be 0–100.")
                tc += fe_g * (fe_w / 100); tw += fe_w

            bonus = min(max(float(self.bonus.get()), 0), 5)
            tc += bonus

            if tw == 0:
                raise ValueError("No assessments entered. Fill in at least one section.")
            if tw > 100:
                messagebox.showwarning("Warning",
                    "Total weights exceed 100%! GWA is computed on the actual weight sum.")

            gwa    = min((tc / tw) * 100, 100.0)
            status = "PASSED ✅" if gwa >= 60 else "FAILED ❌"
            self.result_lbl.config(text=f"GWA: {gwa:.2f}%  |  {status}")
            self.result_gwa = gwa
            self.grab_release()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

# -----------------------------
# SAVED GRADES VIEWER
# -----------------------------
class SavedGradesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Saved Grades")
        self.configure(bg=BG_MAIN)
        self.geometry("500x440")
        self.resizable(True, True)
        self.minsize(320, 240)

        tk.Label(self, text="📋 Saved Grades", bg=BG_MAIN, fg=FG_TITLE,
                 font=FONT_TITLE).pack(pady=8)

        txt = scrolledtext.ScrolledText(
            self, wrap="word", font=("Courier", 10), bg="white", fg="#333")
        txt.pack(fill="both", expand=True, padx=10, pady=8)

        if not data:
            txt.insert("end", "No grades saved yet.")
        else:
            for uid, ud in data.items():
                txt.insert("end", f"User : {ud['name']}  (ID: {uid})\n")
                txt.insert("end",
                    f"Grade Level: {ud.get('grade_level','N/A')}  "
                    f"Section: {ud.get('section','N/A')}\n")
                for quarter, details in ud.get("quarters", {}).items():
                    txt.insert("end", f"  Quarter: {quarter}\n")
                    for subj in details["subjects"]:
                        txt.insert("end", f"    - {subj['name']}: {subj['gwa']:.2f}%\n")
                    txt.insert("end",
                        f"  Overall GWA: {details['overall_gwa']:.2f}%\n")
                txt.insert("end", "\n" + "─"*40 + "\n\n")
        txt.config(state="disabled")

# -----------------------------
# GWA TABLE WINDOW
# -----------------------------
class GWATableWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("PISAY GWA Table")
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)
        self.minsize(280, 320)

        tk.Label(self, text="===== PISAY GWA TABLE =====",
                 bg=BG_MAIN, fg=FG_TITLE, font=FONT_TITLE).pack(pady=8)

        tbl = tk.Frame(self, bg="white", bd=2, relief="ridge")
        tbl.pack(fill="both", expand=True, padx=20, pady=4)
        tbl.columnconfigure(0, weight=1)
        tbl.columnconfigure(1, weight=1)

        for col, header in enumerate(("Percentage", "GWA")):
            tk.Label(tbl, text=header, bg="white", font=FONT_BOLD,
                     anchor="center").grid(row=0, column=col, sticky="ew", padx=6, pady=4)

        for i, (pct, gwa) in enumerate(GWA_TABLE, start=1):
            bg = "#fff0f5" if i % 2 == 0 else "white"
            tk.Label(tbl, text=pct,  bg=bg, anchor="center").grid(
                row=i, column=0, sticky="ew", padx=6, pady=2)
            tk.Label(tbl, text=gwa,  bg=bg, anchor="center").grid(
                row=i, column=1, sticky="ew", padx=6, pady=2)

        tk.Button(self, text="Close", bg=BTN_BG, command=self.destroy).pack(pady=8)

# -----------------------------
# SEARCH USER WINDOW
# -----------------------------
class SearchUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Search User")
        self.configure(bg=BG_MAIN)
        self.geometry("440x400")
        self.resizable(True, True)
        self.minsize(300, 240)

        tk.Label(self, text="🔍 Search User", bg=BG_MAIN, fg=FG_TITLE,
                 font=FONT_TITLE).pack(pady=8)

        top = tk.Frame(self, bg=BG_MAIN)
        top.pack(fill="x", padx=10, pady=4)
        tk.Label(top, text="User ID:", bg=BG_MAIN).pack(side="left")
        self.id_entry = tk.Entry(top, width=20)
        self.id_entry.pack(side="left", padx=6, fill="x", expand=True)
        tk.Button(top, text="Search", bg=BTN_BG, command=self._search).pack(side="left")

        self.result_txt = scrolledtext.ScrolledText(
            self, wrap="word", font=("Courier", 10), bg="white", fg="#333")
        self.result_txt.pack(fill="both", expand=True, padx=10, pady=8)
        self.result_txt.config(state="disabled")

    def _search(self):
        uid = self.id_entry.get().strip()
        self.result_txt.config(state="normal")
        self.result_txt.delete("1.0", "end")
        if uid in data:
            ud = data[uid]
            self.result_txt.insert("end", f"Found: {ud['name']} (ID: {uid})\n")
            self.result_txt.insert("end",
                f"Grade Level: {ud.get('grade_level','N/A')}  "
                f"Section: {ud.get('section','N/A')}\n\n")
            for q, details in ud.get("quarters", {}).items():
                self.result_txt.insert("end", f"  Quarter: {q}\n")
                for subj in details["subjects"]:
                    self.result_txt.insert("end",
                        f"    - {subj['name']}: {subj['gwa']:.2f}%\n")
                self.result_txt.insert("end",
                    f"  Overall GWA: {details['overall_gwa']:.2f}%\n\n")
        else:
            self.result_txt.insert("end", "User not found.")
        self.result_txt.config(state="disabled")

# -----------------------------
# MAIN APPLICATION
# -----------------------------
class GWAApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("GWA Calculator 🌸")
        root.geometry("440x700")
        root.minsize(360, 500)
        root.configure(bg=BG_MAIN)
        root.resizable(True, True)

        # Outer container stretches with the window
        outer = tk.Frame(root, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=10, pady=10)

        # Main scrollable panel with a white ridge frame look
        sf = ScrollableFrame(outer, bg=BG_FRAME)
        sf.configure(bd=2, relief="ridge")
        sf.pack(fill="both", expand=True)

        self.f = sf.inner
        self.f.columnconfigure(0, weight=1)   # single column stretches

        self._build_ui()

    def _build_ui(self):
        f   = self.f
        pad = {"padx": 8, "pady": 3}

        # Title
        tk.Label(f, text="🌸 GWA Calculator 🌸", bg=BG_FRAME, fg=FG_TITLE,
                 font=FONT_TITLE).pack(pady=10, fill="x")

        # ── Student Info ──────────────────────────────────────────────
        info = tk.LabelFrame(f, text=" Student Info ", bg=BG_FRAME,
                             font=FONT_BOLD, fg="#cc0066")
        info.pack(fill="x", padx=10, pady=4)
        info.columnconfigure(1, weight=1)

        for r, (lbl, attr) in enumerate([
            ("Full Name:",        "name_entry"),
            ("ID:",               "id_entry"),
            ("Grade Level:",      "grade_lvl_entry"),
            ("Section:",          "section_entry"),
            ("Quarter (Q1–Q4):", "quarter_entry"),
        ]):
            tk.Label(info, text=lbl, bg=BG_FRAME, anchor="e", width=16).grid(
                row=r, column=0, **pad)
            e = tk.Entry(info)
            e.grid(row=r, column=1, sticky="ew", **pad)
            setattr(self, attr, e)

        tk.Button(info, text="🔍 View Previous Grades", bg=BTN_BG, font=("Arial", 9),
                  command=self._open_search).grid(
            row=5, column=0, columnspan=2, pady=6, sticky="ew", padx=8)

        # ── Subjects ─────────────────────────────────────────────────
        subj_frame = tk.LabelFrame(f, text=" Subjects ", bg=BG_FRAME,
                                   font=FONT_BOLD, fg="#cc0066")
        subj_frame.pack(fill="x", padx=10, pady=4)
        subj_frame.columnconfigure(0, weight=1)

        top_row = tk.Frame(subj_frame, bg=BG_FRAME)
        top_row.pack(fill="x", **pad)
        tk.Label(top_row, text="Number of subjects:", bg=BG_FRAME).pack(side="left")
        self.num_sub = tk.Spinbox(top_row, from_=1, to=15, width=4)
        self.num_sub.pack(side="left", padx=6)

        self.subjects_listbox = tk.Listbox(
            subj_frame, height=6, font=FONT_MONO, selectmode="single",
            activestyle="dotbox")
        self.subjects_listbox.pack(fill="x", padx=8, pady=4)

        btn_row = tk.Frame(subj_frame, bg=BG_FRAME)
        btn_row.pack(pady=4)
        tk.Button(btn_row, text="+ Add Subject",  bg=BTN_BG,  font=FONT_BTN,
                  command=self._add_subject).pack(side="left", padx=4)
        tk.Button(btn_row, text="🗑 Remove Last", bg=BTN_DEL, font=("Arial", 9),
                  command=self._remove_last_subject).pack(side="left", padx=4)

        self.subjects_data: list = []

        # ── Calculate GWA ────────────────────────────────────────────
        tk.Button(f, text="📊 Calculate Overall GWA", bg="#ff66aa", fg="white",
                  font=("Arial", 11, "bold"),
                  command=self._calculate_overall).pack(
            fill="x", padx=10, pady=8)

        self.result_label = tk.Label(
            f, text="", bg=BG_FRAME, fg=FG_TITLE,
            font=("Arial", 12, "bold"), wraplength=360, justify="center")
        self.result_label.pack(pady=2)

        self.equiv_label = tk.Label(f, text="", bg=BG_FRAME)
        self.equiv_label.pack()

        # ── Desired Grade ─────────────────────────────────────────────
        des = tk.LabelFrame(f, text=" --- Desired Grade (%) --- ", bg=BG_FRAME,
                            font=FONT_BOLD, fg="#cc0066")
        des.pack(fill="x", padx=10, pady=4)
        des.columnconfigure(1, weight=1)

        for r, (lbl, attr) in enumerate([
            ("Current Grade:",        "current_entry"),
            ("Desired Grade:",        "desired_entry"),
            ("Remaining Weight (%):", "weight_entry2"),
        ]):
            tk.Label(des, text=lbl, bg=BG_FRAME, anchor="e", width=22).grid(
                row=r, column=0, **pad)
            e = tk.Entry(des, width=10)
            e.grid(row=r, column=1, sticky="ew", **pad)
            setattr(self, attr, e)

        tk.Button(des, text="Calculate Needed", bg=BTN_BG, font=FONT_BTN,
                  command=self._calculate_desired).grid(
            row=3, column=0, columnspan=2, pady=6, sticky="ew", padx=8)

        self.desired_label = tk.Label(
            des, text="", bg=BG_FRAME, font=("Arial", 10, "bold"),
            fg="#555", wraplength=340)
        self.desired_label.grid(row=4, column=0, columnspan=2, pady=4)

        # ── Bottom Buttons ────────────────────────────────────────────
        btm = tk.Frame(f, bg=BG_FRAME)
        btm.pack(fill="x", padx=10, pady=8)
        for col, (text, cmd, bg) in enumerate([
            ("📋 GWA Table",      lambda: GWATableWindow(self.root),    BTN_BG),
            ("💾 View All Saved", lambda: SavedGradesWindow(self.root), BTN_BG),
            ("🔄 Reset",          self._reset,                          BTN_DEL),
        ]):
            btm.columnconfigure(col, weight=1)
            tk.Button(btm, text=text, bg=bg, font=FONT_BTN, command=cmd).grid(
                row=0, column=col, sticky="ew", padx=3)

    def _add_subject(self):
        num = int(self.num_sub.get())
        if len(self.subjects_data) >= num:
            messagebox.showinfo("Info",
                f"Already added {num} subject(s). Increase the count to add more.")
            return

        idx  = len(self.subjects_data) + 1
        name = simpledialog.askstring(
            "Subject Name", f"Enter name for Subject #{idx}:",
            parent=self.root)
        if not name:
            return

        dlg = SubjectDialog(self.root, name)
        self.root.wait_window(dlg)

        if dlg.result_gwa is None:
            messagebox.showinfo("Cancelled", f"No GWA recorded for '{name}'.")
            return

        self.subjects_data.append({"name": name, "gwa": dlg.result_gwa})
        status = "PASSED ✅" if dlg.result_gwa >= 60 else "FAILED ❌"
        self.subjects_listbox.insert(
            "end", f"{name}: {dlg.result_gwa:.2f}%  {status}")

    def _remove_last_subject(self):
        if self.subjects_data:
            self.subjects_data.pop()
            self.subjects_listbox.delete("end")

    def _calculate_overall(self):
        if not self.subjects_data:
            messagebox.showwarning("No Subjects", "Add at least one subject first.")
            return

        name    = self.name_entry.get().strip()
        uid     = self.id_entry.get().strip()
        glevel  = self.grade_lvl_entry.get().strip()
        section = self.section_entry.get().strip()
        quarter = self.quarter_entry.get().strip().upper()

        if not all([name, uid, glevel, section, quarter]):
            messagebox.showwarning("Missing Info", "Fill in all Student Info fields.")
            return
        if quarter not in ("Q1", "Q2", "Q3", "Q4"):
            messagebox.showwarning("Invalid Quarter", "Quarter must be Q1, Q2, Q3, or Q4.")
            return

        current_gwa = cap_gwa(
            sum(s["gwa"] for s in self.subjects_data) / len(self.subjects_data))

        prev_gwa = get_previous_quarter_grade(uid, quarter)
        if prev_gwa is not None:
            overall_gwa = apply_carry(prev_gwa, current_gwa)
            order   = ["Q1", "Q2", "Q3", "Q4"]
            prev_q  = order[order.index(quarter) - 1]
            carry_msg = f"\n(1/3 carry-over from {prev_q}: {prev_gwa:.2f}%)"
        else:
            overall_gwa = current_gwa
            carry_msg   = ""

        save_grade_json(uid, name, glevel, section, quarter,
                        self.subjects_data, overall_gwa)

        gwa_equiv = convert_to_GWA(overall_gwa)
        status    = "PASSED ✅" if overall_gwa >= 60 else "FAILED ❌"

        self.result_label.config(
            text=f"Overall GWA: {overall_gwa:.2f}%  |  {status}{carry_msg}")
        self.equiv_label.config(text=f"GWA Equivalent: {gwa_equiv}")
        messagebox.showinfo("Saved",
            f"Grades saved for {name} ({uid}) in {quarter}.")
        
    def _calculate_desired(self):
        try:
            result = calculate_required_score(
                float(self.current_entry.get()),
                float(self.desired_entry.get()),
                float(self.weight_entry2.get()),
            )
            self.desired_label.config(text=result)
        except ValueError:
            messagebox.showerror("Error",
                "Enter valid numbers in all Desired Grade fields.")

    def _open_search(self):
        SearchUserWindow(self.root)

    def _reset(self):
        if messagebox.askyesno("Reset", "Clear all entered data for this session?"):
            self.subjects_data.clear()
            self.subjects_listbox.delete(0, "end")
            for attr in ("name_entry", "id_entry", "grade_lvl_entry",
                         "section_entry", "quarter_entry",
                         "current_entry", "desired_entry", "weight_entry2"):
                getattr(self, attr).delete(0, "end")
            self.result_label.config(text="")
            self.equiv_label.config(text="")
            self.desired_label.config(text="")
            
# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    GWAApp(root)
    root.mainloop()
