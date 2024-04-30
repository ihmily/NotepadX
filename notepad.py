import os
import webbrowser
from datetime import datetime
from tkinter import scrolledtext, filedialog, messagebox, font, simpledialog
import ctypes
import tkinter as tk
from typing import Literal

filename = ""
font_size = 18
file_modified = False


def zoom_in(_event=None):
    global font_size
    font_size += 1
    change_font(font_size)


def zoom_out(_event=None):
    global font_size
    font_size = max(1, font_size - 1)
    change_font(font_size)


def reset_zoom(_event=None):
    global font_size
    font_size = 18
    change_font(font_size)


def change_font(size):
    scr.configure(font=('微软雅黑', size))


def toggle_wrap(_event=None):
    wrap_var.set(not wrap_var.get())
    if wrap_var.get() == 0:
        new_wrap: Literal["none", "char", "word"] = "none"
    else:
        new_wrap: Literal["none", "char", "word"] = "word"
    scr.configure(wrap=new_wrap)
    style_menu.entryconfigure("自动换行(W)", variable=wrap_var.get())


def update_status_bar(_event=None):
    status_bar_var.set(not status_bar_var.get())

    if wrap_var.get() == 0:
        status_bar.config(text=f"就绪")
    else:
        status_bar.config(text=f"就绪 | 编码: utf-8 | 缩放: 100%")

    view_menu.entryconfigure("状态栏(S)", variable=status_bar_var.get())


def set_font():
    font_name_ = simpledialog.askstring("字体设置", "请输入字体名称:")
    font_size_ = simpledialog.askinteger("字体设置", "请输入字体大小:")

    if font_name_ is None or font_size_ is None:
        return

    selected_font = font.Font(family=font_name_, size=font_size_)
    scr.configure(font=selected_font)


def now_time(_event=None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scr.insert("insert", current_time)


def find():
    def find_text():
        text_to_find = find_entry.get()

        if not text_to_find:
            return

        start_pos = scr.search(text_to_find, "1.0", stopindex="end", nocase=True)

        if start_pos:
            end_pos = f"{start_pos}+{len(text_to_find)}c"
            scr.tag_remove("found", "1.0", "end")
            scr.tag_add("found", start_pos, end_pos)
            scr.tag_configure("found", background="yellow")
            scr.mark_set("insert", start_pos)
            scr.see(start_pos)
            find_text.start_pos = end_pos
        else:
            messagebox.showinfo("查找", f"找不到 '{text_to_find}'")

    def find_next():
        text_to_find = find_entry.get()

        if not text_to_find:
            return
        if hasattr(find_text, 'start_pos'):
            start_pos = scr.search(text_to_find, find_text.start_pos, stopindex="end", nocase=True)

            if start_pos:
                end_pos = f"{start_pos}+{len(text_to_find)}c"
                scr.tag_remove("found", "1.0", "end")
                scr.tag_add("found", start_pos, end_pos)
                scr.tag_configure("found", background="yellow")
                scr.mark_set("insert", start_pos)
                scr.see(start_pos)
                find_text.start_pos = end_pos
            else:
                messagebox.showinfo("查找", f"找不到更多 '{text_to_find}'")
        else:
            messagebox.showinfo("查找", f"找不到更多 '{text_to_find}'")

    find_window = tk.Toplevel(root)
    find_window.title("查找")

    tk.Label(find_window, text="查找内容:").grid(row=0, column=0)
    find_entry = tk.Entry(find_window, width=30)
    find_entry.grid(row=0, column=1)

    find_button = tk.Button(find_window, text="查找", command=find_text)
    find_button.grid(row=1, column=0, padx=5, pady=5)
    find_next_button = tk.Button(find_window, text="查找下一个", command=find_next)
    find_next_button.grid(row=1, column=1, padx=5, pady=5)

    find_entry.focus_set()

    find_window.attributes('-topmost', True)

    find_window.update_idletasks()
    screen_width = find_window.winfo_screenwidth()
    screen_height = find_window.winfo_screenheight()
    window_width = find_window.winfo_width()
    window_height = find_window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    find_window.geometry(f"+{x}+{y}")


def replace():
    def replace_text():
        text_to_replace = replace_entry.get()
        text_to_find = find_entry.get()

        if not text_to_replace or not text_to_find:
            return

        start_pos = scr.search(text_to_find, "1.0", stopindex="end", nocase=True)
        while start_pos:
            end_pos = f"{start_pos}+{len(text_to_find)}c"
            scr.delete(start_pos, end_pos)
            scr.insert(start_pos, text_to_replace)

            start_pos = scr.search(text_to_find, end_pos, stopindex="end", nocase=True)

    replace_window = tk.Toplevel(root)
    replace_window.title("替换")

    tk.Label(replace_window, text="查找内容:").grid(row=0, column=0)
    find_entry = tk.Entry(replace_window, width=30)
    find_entry.grid(row=0, column=1)

    tk.Label(replace_window, text="替换为:").grid(row=1, column=0)
    replace_entry = tk.Entry(replace_window, width=30)
    replace_entry.grid(row=1, column=1)

    replace_button = tk.Button(replace_window, text="替换", command=replace_text)
    replace_button.grid(row=2, column=0, columnspan=2, pady=5)

    find_entry.focus_set()

    replace_window.update_idletasks()
    screen_width = replace_window.winfo_screenwidth()
    screen_height = replace_window.winfo_screenheight()
    window_width = replace_window.winfo_width()
    window_height = replace_window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    replace_window.geometry(f"+{x}+{y}")

    replace_window.attributes('-topmost', True)


def cut():
    try:
        scr.clipboard_clear()
        scr.clipboard_append(scr.selection_get())
        scr.delete(tk.SEL_FIRST, tk.SEL_LAST)  # 删除选中内容
    except Exception as e:
        print('cut error', e)


def copy():
    try:
        # 检查是否有选中的文本
        if scr.tag_ranges(tk.SEL):
            scr.clipboard_clear()  # 清除剪贴板
            scr.clipboard_append(scr.selection_get())  # 复制选中的文本
    except Exception as e:
        print('copy error', e)


def paste():
    try:
        if scr.tag_ranges(tk.SEL):
            scr.delete(tk.SEL_FIRST, tk.SEL_LAST)
        scr.insert(tk.INSERT, scr.clipboard_get())
    except Exception as e:
        print('paste error', e)


def openfile(_event=None):
    global filename
    if check_and_newfile():
        filename = filedialog.askopenfilename(title='打开文件', filetypes=[('文本文件', '.txt'), ('All File', '*.*')])
        print(filename)
        if filename == "":
            filename = None
        else:
            root.title(os.path.basename(filename) + " - 记事本")
            scr.delete(1.0, tk.END)
            f1 = open(filename, 'r', encoding='utf-8')
            a = f1.read()
            f1.readlines()
            scr.insert(tk.INSERT, a)
            f1.close()


def ask_save():
    global file_modified, filename
    response = messagebox.askyesnocancel("保存", "是否保存当前更改？")
    if response:  # 保存
        if filename:
            savefile()
        else:
            if not savefile_as():
                return False
    elif response is None:
        return False
    else:
        pass
    file_modified = False
    return True


def savefile(_event=None):
    global filename, file_modified
    try:
        if os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                b = scr.get(0.0, tk.END)
                f.write(b)
            file_modified = False
        else:
            savefile_as()
    except Exception as e:
        print(e)
        savefile_as()


def savefile_as(_event=None):
    global filename, file_modified
    try:
        fpath = filedialog.asksaveasfilename(title='另存为',
                                             initialfile='文本.txt', defaultextension=".txt",
                                             filetypes=[('文本文件', '.txt'), ('All File', '*.*')])
        if fpath:
            f2 = open(fpath, 'w', encoding='utf-8')
            b = scr.get(0.0, tk.END)
            f2.write(b)
            f2.close()
            root.title(os.path.basename(fpath) + " - 记事本")
            file_modified = False
            filename = fpath
            return True
    except Exception as e:
        print(e)
    return False


def undo():
    global scr
    scr.event_generate("<<Undo>>")


def delete():
    try:
        scr.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except Exception as e:
        print('delete error', e)


def to_exit(_event=None):
    if check_and_newfile():
        root.destroy()


def show_about():
    about_text = """
    关于 记事本
    版本: 1.0
    开发者: Hmily
    一个简单易用的文本编辑工具，允许用户快速打开、编辑和保存文本文件。
    感谢您选择使用本软件，我们希望它能满足您的需要。
    官方网站: https://github.com/ihmily/NotepadX
    """
    messagebox.showinfo("关于 记事本", about_text)


def help_web():
    webbrowser.open("https://github.com/ihmily/NotepadX")


def check_and_newfile(_event=None):
    global file_modified
    if file_modified:
        return ask_save()
    return True


def newfile(_event=None):
    global root, filename, scr, file_modified
    if check_and_newfile():
        root.title("未命名文件")
        filename = None
        scr.delete(1.0, tk.END)
        file_modified = False
        root.title("未命名文件 - 记事本")


def text_modified(_event=None):
    global file_modified
    file_modified = True


def select_all():
    global scr
    scr.tag_add("sel", "1.0", "end")


root = tk.Tk()
root.geometry("1100x700+400+100")
root.title('记事本')
# root.iconbitmap('favicon.ico')
ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', scale_factor / 75)

status_bar = tk.Label(root, text='就绪', bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# 创建主菜单栏
menubar = tk.Menu(root)

# 创建菜单
file_menu = tk.Menu(menubar, tearoff=0)
edit_menu = tk.Menu(menubar, tearoff=0)
style_menu = tk.Menu(menubar, tearoff=0)
view_menu = tk.Menu(menubar, tearoff=0)
help_menu = tk.Menu(menubar, tearoff=0)

# 将菜单加入到主菜单栏
menubar.add_cascade(label="文件(F)", menu=file_menu)
menubar.add_cascade(label="编辑(E)", menu=edit_menu)
menubar.add_cascade(label="格式(O)", menu=style_menu)
menubar.add_cascade(label="查看(V)", menu=view_menu)
menubar.add_cascade(label="帮助(H)", menu=help_menu)

# 添加子菜单项-文件
file_menu.add_command(label="新建(N)", accelerator="Ctrl+N", command=newfile)
file_menu.add_command(label="新窗口(W)", accelerator="Ctrl+W")
file_menu.add_command(label="打开(O)", accelerator="Ctrl+O", command=openfile)
file_menu.add_command(label="保存(S)", accelerator="Ctrl+S", command=savefile)
file_menu.add_command(label="另存为A)", accelerator="Ctrl+Shift+S", command=savefile_as)
file_menu.add_separator()  # 添加分割线
file_menu.add_command(label="退出(X)", command=to_exit)

# 添加子菜单项-编辑
edit_menu.add_command(label="撤销(U)", accelerator="Ctrl+Z", command=undo)
edit_menu.add_separator()  # 添加分割线
edit_menu.add_command(label="剪切(T)", accelerator="Ctrl+X", command=cut)
edit_menu.add_command(label="复制(C)", accelerator="Ctrl+C", command=copy)
edit_menu.add_command(label="粘贴(V)", accelerator="Ctrl+V", command=paste)
edit_menu.add_command(label="删除(L)", accelerator="Del", command=delete)
edit_menu.add_separator()  # 添加分割线
edit_menu.add_command(label="查找(F)", accelerator="Ctrl+F", command=find)
edit_menu.add_command(label="替换(R)", accelerator="Ctrl+H", command=replace)
edit_menu.add_separator()  # 添加分割线
edit_menu.add_command(label="全选(A)", accelerator="Ctrl+A", command=select_all)
edit_menu.add_command(label="时间/日期(D)", accelerator="F5", command=now_time)

wrap_var = tk.IntVar()
wrap_var.set(1)
style_menu.add_checkbutton(label="自动换行(W)", variable=wrap_var, command=toggle_wrap)
style_menu.add_command(label="字体(F)", command=set_font)

# 添加子菜单项-查看
menuZoom = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="缩放(Z)", menu=menuZoom)  # 添加子子菜单
menuZoom.add_command(label="放大(I)", accelerator="Ctrl+加号", command=zoom_in)
menuZoom.add_command(label="缩小(O)", accelerator="Ctrl+减号", command=zoom_out)
menuZoom.add_command(label="恢复默认缩放", accelerator="Ctrl+O", command=reset_zoom)
status_bar_var = tk.IntVar()
status_bar_var.set(0)
view_menu.add_checkbutton(label="状态栏(S)", variable=status_bar_var, command=update_status_bar)

# 添加子菜单项-帮助
help_menu.add_command(label="查看帮助(H)", command=help_web)
help_menu.add_command(label="发送反馈(F)")
help_menu.add_command(label="关于记事本(A)", command=show_about)

# 将主菜单栏加到根窗口
root["menu"] = menubar
scr = scrolledtext.ScrolledText(root, width=75, height=22, font=('微软雅黑', 18), undo=True)
scr.pack(expand=tk.YES, fill=tk.BOTH)

# 热键绑定
scr.bind("<Control-n>", newfile)
scr.bind("<Control-N>", newfile)
scr.bind("<Control-o>", openfile)
scr.bind("<Control-O>", openfile)
scr.bind("<Control-S>", savefile)
scr.bind("<Control-s>", savefile)
scr.bind("<Control-Shift-S>", savefile_as)
scr.bind("<Control-Shift-s>", savefile_as)
scr.bind("<Control-Shift-x>", to_exit)
scr.bind("<Control-Shift-X>", to_exit)
scr.bind("<Control-F>", find)
scr.bind("<Control-f>", find)
scr.bind("<Control-H>", replace)
scr.bind("<Control-h>", replace)
scr.bind("<Control-W>", toggle_wrap)
scr.bind("<Control-w>", toggle_wrap)
scr.bind("<F5>", now_time)
scr.bind("<Control-plus>", zoom_in)
scr.bind("<Control-minus>", zoom_out)
scr.bind("<Control-0>", reset_zoom)
scr.bind("<KeyRelease>", text_modified)


def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)


# 创建右键菜单
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="复制", command=copy)
context_menu.add_command(label="粘贴", command=paste)
context_menu.add_separator()
context_menu.add_command(label="剪切", command=cut)
context_menu.add_command(label="全选", command=select_all)

# 将右键菜单与文本框绑定
scr.bind("<Button-3>", show_context_menu)

root.mainloop()
