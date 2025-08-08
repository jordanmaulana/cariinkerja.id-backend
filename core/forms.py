from django import forms
from django.contrib.auth.forms import SetPasswordForm


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Kata Sandi Baru",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text='<ul class="help-text"><li>Kata sandi Anda tidak boleh terlalu mirip dengan informasi pribadi Anda yang lain.</li><li>Kata sandi Anda harus mengandung setidaknya 8 karakter.</li><li>Kata sandi Anda tidak boleh menjadi kata sandi yang umum digunakan.</li><li>Kata sandi Anda tidak boleh seluruhnya numerik.</li></ul>',
    )
    new_password2 = forms.CharField(
        label="Konfirmasi Kata Sandi Baru",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
