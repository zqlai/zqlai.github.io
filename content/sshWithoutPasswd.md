Title: setting for ssh login without password input
Category: Linux
Tags: ssh
Authors: zqlai


just two steps

1.generate key pairs if not exist

```
ssh-keygen -t rsa
```

If success, you will find `id_rsa` and `id_rsa.pub` in the `~/.ssh/` dir

2.copy the public key to the server you want to login
```
ssh-copy-id username@hostname
```
Then, it will authorize your permission by password.

If both steps is done, you can ssh to the server without password input.
In the ~/.ssh/authorized_key file on the server, you will find an entry like:
```
sh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCpwXmBPQcLBDDZxUa18bLHoL0WrCRx9KR/4Dryyp4bbqq9877/hYQCKq9Cxvjvo6pBkQB6DdykEHnJIVKhgGGt1y85L0IYTkazM8O4Q04sj/RhBvscf5fOdSedRu7UVzULVccBrm1/uzfDZQnUgDUTrmGe3ynGVU0tjxwjXay5Xj7KZJmggGKR40bQ3eZAiXGbQSDSYaF9teT1aLh6z3Z0Z/7g7EtOwBWRrWoLlhgNiBF7uHi4FGlHxj2u9jcRTKzdI/rfTaVJZNyVuS7sSUqDl7fGyQ1XJq4AEKZg/wRuomKlme7aLl9Ee+8Lj+/kpdEcRYNImJHV9CdTKYZXNIFZ XX@XX
```
