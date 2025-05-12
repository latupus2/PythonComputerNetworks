# Task9: Сравнение IPv4 и IPv6

---
## Настройка Docker Desktop
settings -> docker engine -> вставьте:  
```
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64",
  "experimental": true
}
```

---
## Создание сети с IPv6
```
docker network create --ipv6 ipv6_net
```

---
## Запуск контейнеров с IPv6
```
docker run -itd --network=ipv6_net --name=test_container1 alpine
docker run -itd --network=ipv6_net --name=test_container2 alpine
```

---
## Проверка IPv4-адресов
```
docker exec test_container1 ip -4 addr show
docker exec test_container2 ip -4 addr show
```

---
## Проверка IPv6-адресов
```
docker exec test_container1 ip -6 addr show
docker exec test_container2 ip -6 addr show
```

---
## Тесты
```
docker exec test_container1 ping -c 4 <IPv4_адрес_test_container2>
docker exec test_container1 ping6 -c 4 <IPv6_адрес_test_container2>
```

---
## Результаты
Для просмотра результатов используйте Wireshark.
