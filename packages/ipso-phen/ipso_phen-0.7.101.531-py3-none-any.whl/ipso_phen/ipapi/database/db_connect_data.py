db_connect_data = {
    "phenoserre": {
        "user": "pheno_user",
        "password": "p1h2e3!",
        "port": 22,
        "jump_address": "genologin.toulouse.inra.fr",
        "target_address": "147.99.108.65",
        "query_root": 'psql -A -F , -q -P "footer=off" -d LemnaTecOptimalogTest -U phenodbpg -c ',
        "exp_list_query": "select distinct measurement_label from snapshot",
    },
    "phenopsis": {
        "user": "pheno_user",
        "password": "p1h2e3!",
        "port": 22,
        "address": "genologin.toulouse.inra.fr",
        "target_address": "147.99.108.65",
        "query_root": 'psql -A -F , -q -P "footer=off" -d LemnaTecOptimalogTest -U phenodbpg -c ',
        "exp_list_query": "select distinct measurement_label from snapshot",
    },
    "mass_storage": {
        "folder_names": ["images", "input"],
    },
    "psql_local": True,
}
