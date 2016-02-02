FROM python:2-onbuild
CMD /usr/local/bin/gunicorn webapp:app -w 2 -b :8000
EXPOSE 8000
