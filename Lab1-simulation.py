from itertools import accumulate


iat_dist = {1: 0.25, 2: 0.40, 3: 0.20, 4: 0.15}
able_dist = {2: 0.30, 3: 0.28, 4: 0.25, 5: 0.17}
baker_dist = {2: 0.35, 3: 0.25, 4: 0.20, 5: 0.20}


def build_table(dist):
    """بترجع list من (value, prob, cumulative, low, high) ."""
    values = list(dist.keys())
    probs = list(dist.values())
    cums = [round(c, 2) for c in accumulate(probs)]
    table = []
    low = 1
    for v, p, c in zip(values, probs, cums):
        high = round(c * 100)         
        table.append((v, p, c, low, high))
        low = high + 1
    return table


def lookup(table, rn):
    """بتحول الـ random number لقيمة. الرقم 00 بيتعامل كأنه 100."""
    rn = 100 if rn == 0 else rn
    for v, _, _, low, high in table:
        if low <= rn <= high:
            return v
    raise ValueError(f"RN {rn} out of range")


def print_table(name, table):
    print(f"\n{name}")
    print(f"{'Value':<8}{'Prob':<8}{'Cum':<8}{'RN range'}")
    for v, p, c, low, high in table:
        hi = "00" if high == 100 else f"{high:02d}"
        print(f"{v:<8}{p:<8.2f}{c:<8.2f}{low:02d}-{hi}")


iat_table = build_table(iat_dist)
able_table = build_table(able_dist)
baker_table = build_table(baker_dist)

print_table("Inter-arrival time", iat_table)
print_table("Able service time", able_table)
print_table("Baker service time", baker_table)


iat_rns = [26, 98, 90, 26, 42, 74, 80, 68, 22, 48, 34, 45, 24,
           34, 63, 38, 80, 42, 56, 89, 18, 51, 71, 16, 92]
service_rns = [95, 21, 51, 92, 89, 38, 13, 61, 50, 49, 39, 53, 88,
               1, 81, 53, 81, 64, 1, 67, 1, 47, 75, 57, 87, 47]

#
SIM_TIME = 60            
free_at = {"Baker": 0, "Able": 0}   

arrival = 0
rows = []
for i, rn_service in enumerate(service_rns):
    if i > 0:
        arrival += lookup(iat_table, iat_rns[i - 1])
    if arrival > SIM_TIME:
        break

    # choose server
    free_servers = [s for s in free_at if free_at[s] <= arrival]
    if free_servers:
        server = free_servers[0]
    else:
        server = min(free_at, key=lambda s: free_at[s])

    table = baker_table if server == "Baker" else able_table
    service = lookup(table, rn_service)
    start = max(arrival, free_at[server])
    end = start + service
    free_at[server] = end

    rows.append((i + 1, arrival, rn_service, server, start, service, end, start - arrival))

#Tabl of simulation results
print("\n{:<5}{:<9}{:<6}{:<8}{:<7}{:<9}{:<7}{}".format(
    "Cust", "Arrival", "RN", "Server", "Start", "Service", "End", "Wait"))
for r in rows:
    print("{:<5}{:<9}{:<6}{:<8}{:<7}{:<9}{:<7}{}".format(*r))

