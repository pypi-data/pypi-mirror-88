import setuptools

with open("Kaptsja/README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kaptsja", # Replace with your own username
    version="10.1.5",
    author="Peter Stamps",
    author_email="p.j.m.stamps@gmail.com",
    description="Kaptsja is the Dutch 'phonetic pronunciation' for this CaptCha software with special and complex features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peterstamps/Kaptsja/",
    project_urls={
    'Documentation': 'https://github.com/peterstamps/Kaptsja'},
    # packages=setuptools.find_packages(),
    packages=setuptools.find_packages(include=['Kaptsja', 'Kaptsja.*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
    ],
    keywords='Captcha catpcha, recaptcha, re-captcha Encryption Decryption Picture Puzzle Circle Character Generator',
    tag='http bottle web server proxy http proxy server proxy server http server http web server proxy framework web framework Python3 catpcha recaptcha re-captcha hcaptcha google cloud mitm man in the middle web server web scraping botting bottle encrypt encryption decrypt decryption AES picture image PIL pillow puzzle',
    license_file  = "Kaptsja Copyright Notice.txt",
    install_requires=[],
    python_requires='>=3.7.4',
    scripts=[],
    # package_dir={'': ''},
    data_files=[
                ('Kaptsja/.', ['Kaptsja/Kaptsja Copyright Notice.txt', 'Kaptsja/Readme.rst','Kaptsja/Start_Kaptsja_website.bat','Kaptsja/Start_Kaptsja_website.sh']),
                ('Kaptsja/css', ['Kaptsja/css/bootstrap.min-3.3.7.css']),
                ('Kaptsja/docs', ['Kaptsja/docs/Installation_of_Kaptsja_with_ginx_and_uwsgi.rst', 'Kaptsja/docs/Readme2.rst']),
                ('Kaptsja/html', ['Kaptsja/html/KaptsjaFailurePage.html', 'Kaptsja/html/KaptsjaHome.html', 'Kaptsja/html/KaptsjaSuccessPage.html']),
                ('Kaptsja/js', ['Kaptsja/js/bootstrap.min-3.3.7.js', 'Kaptsja/js/jquery.min-3.5.1.js']),
                ('Kaptsja/key', ['Kaptsja/key/place_holder_delete_me.txt']),
                ('Kaptsja/log', ['Kaptsja/log/Kaptsja.log']),
                ('Kaptsja/media', ['Kaptsja/media/Glass_1.jpg', 'Kaptsja/media/Glass_2.jpg', 'Kaptsja/media/Glass_3.jpg', 'Kaptsja/media/Glass_4.jpg', 'Kaptsja/media/Glass_5.jpg', 'Kaptsja/media/Glass_6.jpg', 'Kaptsja/media/Glass_7.jpg', 'Kaptsja/media/Glass_8.jpg', 'Kaptsja/media/Kaptsja.ico', 'Kaptsja/media/Kaptsja_bg.jpg']),
                ('Kaptsja/media/randomlist', ['Kaptsja/media/randomlist/Glass_1.jpg', 'Kaptsja/media/randomlist/Glass_2.jpg', 'Kaptsja/media/randomlist/Glass_3.jpg', 'Kaptsja/media/randomlist/Glass_4.jpg', 'Kaptsja/media/randomlist/Glass_5.jpg', 'Kaptsja/media/randomlist/Glass_6.jpg', 'Kaptsja/media/randomlist/Glass_7.jpg', 'Kaptsja/media/randomlist/Glass_8.jpg', ]),
                ('Kaptsja/scripts', ['Kaptsja/scripts/KaptsjaSite.py', 'Kaptsja/scripts/KaptsjaGenerator.py', 'Kaptsja/scripts/KaptsjaConfiguration.py', 'Kaptsja/scripts/KaptsjaHTMLpages.py', 'Kaptsja/scripts/KaptsjaPictureIco.py', 'Kaptsja/scripts/KaptsjaEncDec.py','Kaptsja/scripts/Z__input.txt', 'Kaptsja/scripts/Z__input_dec.txt', 'Kaptsja/scripts/Z__input_enc.txt']),
                ('Kaptsja/work', ['Kaptsja/work/place_holder_delete_me.txt']),
                ],
)