# Evaluation Report

## Summary

- Generated at `2026-05-20T19:59:16.983748+00:00` UTC
- Repo config `C:\mypc\dev1\code\backend\evaluation\my_eval.json`
- Retrieval questions per repo capped at `120`

### Retrieval metric definitions

| Metric         | Meaning                                                                              |
| -------------- | ------------------------------------------------------------------------------------ |
| Top-1 accuracy | Queries where globally ranked retrieval #1 satisfies the Architecture.md match rules |
| Recall@3       | Queries where positions 1-3 contain at least one match                               |
| Recall@5       | Queries where positions 1-5 contain at least one match                               |

Match rule priority:

1. `file_line_overlap` → Same normalized path + overlapping line spans.
2. `file_symbol_match` → Same path + identical symbol identifiers.
3. `file_only_fallback_missing_metadata` → Either side lacked spans needed for overlap.

## Retrieval metrics

- Total generated questions: `67`
- Macro Top-1: `74.627%`
- Macro Recall@3: `89.552%`
- Macro Recall@5: `95.522%`

### Macro averages

| Repo            | Questions |   Top-1 | Recall@3 | Recall@5 |
| --------------- | --------: | ------: | -------: | -------: |
| Task-Management |        37 | 97.297% |  97.297% |   100.0% |
| Tetris-Game     |        30 | 46.667% |    80.0% |    90.0% |

## Per-repository retrieval details

### Task-Management (`3f27fa80-fb93-4505-b57d-8d120f187c82`)

- Questions evaluated: `37`
| Top-1 | Recall@3 | Recall@5 |
| 97.297% | 97.297% | 100.0% |
<details>

- **Question:** In which file is class `Activity` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L6-24 [read_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L9-15 [Activity.__str__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
```

</details>

---

<details>

- **Question:** Where is method `Activity.getDuration` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.getDuration`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L20-21 [Activity.getDuration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
```

</details>

---

<details>

- **Question:** Where is method `Activity.getEarly` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.getEarly`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L26-27 [Activity.getEarly]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L20-21 [Activity.getDuration]
```

</details>

---

<details>

- **Question:** Where is method `Activity.getLate` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.getLate`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L29-30 [Activity.getLate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L6-24 [read_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
```

</details>

---

<details>

- **Question:** Where is method `Activity.getName` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.getName`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L17-18 [Activity.getName]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L20-21 [Activity.getDuration]
```

</details>

---

<details>

- **Question:** Where is method `Activity.getPrerequisites` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.getPrerequisites`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L23-24 [Activity.getPrerequisites]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L9-15 [Activity.__str__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L6-24 [read_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
```

</details>

---

<details>

- **Question:** Where is method `Activity.setEarly` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.setEarly`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L32-33 [Activity.setEarly]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L26-27 [Activity.getEarly]
```

</details>

---

<details>

- **Question:** Where is method `Activity.setLate` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py` :: `Activity.setLate`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L35-36 [Activity.setLate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L6-24 [read_activities]
```

</details>

---

<details>

- **Question:** Where is function `TopoSort` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `TopoSort`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L57-78 [TopoSortDFS]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
```

</details>

---

<details>

- **Question:** Where is function `TopoSortDFS` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `TopoSortDFS`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L57-78 [TopoSortDFS]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L86-87 [Graph.set_cost]
```

</details>

---

<details>

- **Question:** Where is function `critical_activities` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `critical_activities`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\README.md L1-2 [(whole file)]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
```

</details>

---

<details>

- **Question:** Where is function `early_scheduling` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `early_scheduling`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L32-33 [Activity.setEarly]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\README.md L1-2 [(whole file)]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L26-27 [Activity.getEarly]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L150-171 [scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
```

</details>

---

<details>

- **Question:** Where is function `get_total_duration` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `get_total_duration`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L20-21 [Activity.getDuration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L9-15 [Activity.__str__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
```

</details>

---

<details>

- **Question:** Where is function `graph_from_activities` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `graph_from_activities`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
```

</details>

---

<details>

- **Question:** Where is function `late_scheduling` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `late_scheduling`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\README.md L1-2 [(whole file)]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L150-171 [scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L32-33 [Activity.setEarly]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L35-36 [Activity.setLate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L29-30 [Activity.getLate]
```

</details>

---

<details>

- **Question:** Where is function `map_activities` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `map_activities`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L131-147 [get_total_duration]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
```

</details>

---

<details>

- **Question:** Where is function `read_activities` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `read_activities`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L6-24 [read_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L174-186 [critical_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L27-38 [map_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L9-15 [Activity.__str__]
```

</details>

---

<details>

- **Question:** Where is function `scheduling` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py` :: `scheduling`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L113-128 [late_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\README.md L1-2 [(whole file)]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L150-171 [scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L57-78 [TopoSortDFS]
```

</details>

---

<details>

- **Question:** In which file is class `Graph` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
```

</details>

---

<details>

- **Question:** Where is method `Graph.add_edge` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.add_edge`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L33-44 [Graph.add_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L14-20 [Graph.add_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
```

</details>

---

<details>

- **Question:** Where is method `Graph.add_vertex` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.add_vertex`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L14-20 [Graph.add_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L33-44 [Graph.add_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_cost` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_cost`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L83-84 [Graph.get_cost]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L86-87 [Graph.set_cost]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L33-44 [Graph.add_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_in_degree` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_in_degree`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L77-78 [Graph.get_in_degree]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L80-81 [Graph.get_out_degree]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_in_edges` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_in_edges`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_number_of_edges` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_number_of_edges`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L77-78 [Graph.get_in_degree]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_number_of_vertices` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_number_of_vertices`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_out_degree` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_out_degree`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L80-81 [Graph.get_out_degree]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L77-78 [Graph.get_in_degree]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
```

</details>

---

<details>

- **Question:** Where is method `Graph.get_out_edges` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.get_out_edges`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
```

</details>

---

<details>

- **Question:** Where is method `Graph.is_edge` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.is_edge`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L33-44 [Graph.add_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
```

</details>

---

<details>

- **Question:** Where is method `Graph.is_vertex` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.is_vertex`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L14-20 [Graph.add_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
```

</details>

---

<details>

- **Question:** Where is method `Graph.parse_nin` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.parse_nin`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L22-31 [Graph.remove_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
```

</details>

---

<details>

- **Question:** Where is method `Graph.parse_nout` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.parse_nout`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L22-31 [Graph.remove_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L41-54 [graph_from_activities]
```

</details>

---

<details>

- **Question:** Where is method `Graph.parse_vertices` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.parse_vertices`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L66-70 [Graph.parse_nin]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L22-31 [Graph.remove_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L14-20 [Graph.add_vertex]
```

</details>

---

<details>

- **Question:** Where is method `Graph.remove_edge` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.remove_edge`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L22-31 [Graph.remove_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L46-52 [Graph.remove_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L101-102 [Graph.get_out_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L98-99 [Graph.get_in_edges]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L54-58 [Graph.is_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L95-96 [Graph.get_number_of_edges]
```

</details>

---

<details>

- **Question:** Where is method `Graph.remove_vertex` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.remove_vertex`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L22-31 [Graph.remove_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L14-20 [Graph.add_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L46-52 [Graph.remove_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L92-93 [Graph.get_number_of_vertices]
```

</details>

---

<details>

- **Question:** Where is method `Graph.set_cost` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py` :: `Graph.set_cost`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L1-102 [Graph]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L86-87 [Graph.set_cost]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L83-84 [Graph.get_cost]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L33-44 [Graph.add_edge]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L89-90 [Graph.is_vertex]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L72-75 [Graph.parse_vertices]
```

</details>

---

<details>

- **Question:** Where is function `run` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py` :: `run`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\main.py L4-21 [run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L98-110 [early_scheduling]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L2-7 [Activity.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L32-33 [Activity.setEarly]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\controller.py L81-95 [TopoSort]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L2-12 [Graph.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\activity.py L1-36 [Activity]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Task-Management_3f27fa80\graph.py L60-64 [Graph.parse_nout]
```

</details>

---

### Tetris-Game (`ae028ffa-e679-4289-aba7-b439381af3c2`)

- Questions evaluated: `30`
| Top-1 | Recall@3 | Recall@5 |
| 46.667% | 80.0% | 90.0% |
<details>

- **Question:** In which file is class `App` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py` :: `App`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ❌

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L91-93 [Tetris.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L13-17 [Text.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L17-24 [Technologies 🛠️]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L6-56 [App]
```

</details>

---

<details>

- **Question:** Where is method `App.check_events` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py` :: `App.check_events`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L6-56 [App]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L16-24 [App.set_timer]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
```

</details>

---

<details>

- **Question:** Where is method `App.draw` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py` :: `App.draw`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L91-93 [Tetris.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L30-35 [App.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L13-17 [Text.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L76-79 [Tetris.draw_grid]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L6-56 [App]
```

</details>

---

<details>

- **Question:** Where is method `App.run` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py` :: `App.run`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L91-93 [Tetris.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L6-56 [App]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L16-24 [App.set_timer]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L13-17 [Text.draw]
```

</details>

---

<details>

- **Question:** Where is method `App.set_timer` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py` :: `App.set_timer`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L6-56 [App]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L16-24 [App.set_timer]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L40-42 [Block.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
```

</details>

---

<details>

- **Question:** Where is method `App.update` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py` :: `App.update`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L84-85 [Tetromino.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L40-42 [Block.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L6-56 [App]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
```

</details>

---

<details>

- **Question:** In which file is class `Tetris` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ❌

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L2-8 [Tetris Game 🎮]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
```

</details>

---

<details>

- **Question:** In which file is class `Text` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Text`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L13-17 [Text.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L35-37 [Tetris.get_score]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L17-24 [Technologies 🛠️]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.check_full_lines` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.check_full_lines`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L95-109 [Tetris.check_full_lines]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L35-37 [Tetris.get_score]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.check_tetromino_landing` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.check_tetromino_landing`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.control` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.control`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L65-74 [Tetris.control]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L2-8 [Tetris Game 🎮]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.draw` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.draw`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L30-35 [App.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L91-93 [Tetris.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L8-23 [Block.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L13-17 [Text.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.draw_grid` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.draw_grid`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L76-79 [Tetris.draw_grid]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L91-93 [Tetris.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L8-23 [Block.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L36-38 [Block.set_rect_pos]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.get_field_array` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.get_field_array`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L49-50 [Tetris.get_field_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L44-51 [Block.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.get_score` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.get_score`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L35-37 [Tetris.get_score]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.is_game_over` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.is_game_over`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L39-42 [Tetris.is_game_over]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L2-8 [Tetris Game 🎮]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.put_tetromino_blocks_in_array` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.put_tetromino_blocks_in_array`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L8-23 [Block.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L39-42 [Tetris.is_game_over]
```

</details>

---

<details>

- **Question:** Where is method `Tetris.update` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Tetris.update`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L40-42 [Block.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L84-85 [Tetromino.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L37-49 [App.check_events]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
```

</details>

---

<details>

- **Question:** Where is method `Text.draw` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py` :: `Text.draw`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L13-17 [Text.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L30-35 [App.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L91-93 [Tetris.draw]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L7-14 [App.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L35-37 [Tetris.get_score]
```

</details>

---

<details>

- **Question:** In which file is class `Block` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Block`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L73-82 [Tetromino.move]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L8-17 [Text]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L44-51 [Block.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L62-69 [Tetromino.rotate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L9-11 [Text.__init__]
```

</details>

---

<details>

- **Question:** In which file is class `Tetromino` defined?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Tetromino`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L36-38 [Block.set_rect_pos]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
```

</details>

---

<details>

- **Question:** Where is method `Block.is_alive` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Block.is_alive`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L40-42 [Block.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L39-42 [Tetris.is_game_over]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L73-82 [Tetromino.move]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L52-56 [App.run]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
```

</details>

---

<details>

- **Question:** Where is method `Block.is_collide` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Block.is_collide`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L44-51 [Block.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L73-82 [Tetromino.move]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L62-69 [Tetromino.rotate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L39-42 [Tetris.is_game_over]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L26-28 [Block.is_alive]
```

</details>

---

<details>

- **Question:** Where is method `Block.rotate` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Block.rotate`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L30-34 [Block.rotate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L62-69 [Tetromino.rotate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L73-82 [Tetromino.move]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L65-74 [Tetris.control]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L84-85 [Tetromino.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Block.set_rect_pos` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Block.set_rect_pos`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L40-42 [Block.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L36-38 [Block.set_rect_pos]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L73-82 [Tetromino.move]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L39-42 [Tetris.is_game_over]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
```

</details>

---

<details>

- **Question:** Where is method `Block.update` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Block.update`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L84-85 [Tetromino.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L40-42 [Block.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L45-48 [Tetris.put_tetromino_blocks_in_array]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L73-82 [Tetromino.move]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L39-42 [Tetris.is_game_over]
```

</details>

---

<details>

- **Question:** Where is method `Tetromino.is_collide` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Tetromino.is_collide`

- **Correctness:**
- top-1 ❌
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L44-51 [Block.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L71-72 [Tetromino.is_collide]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L2-8 [Tetris Game 🎮]
```

</details>

---

<details>

- **Question:** Where is method `Tetromino.move` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Tetromino.move`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L65-74 [Tetris.control]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L8-23 [Block.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L7-51 [Block]
```

</details>

---

<details>

- **Question:** Where is method `Tetromino.rotate` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Tetromino.rotate`

- **Correctness:**
- top-1 ✅
- Recall@3 ✅
- Recall@5 ✅

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L65-74 [Tetris.control]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L30-34 [Block.rotate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L62-69 [Tetromino.rotate]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L8-23 [Block.__init__]
```

</details>

---

<details>

- **Question:** Where is method `Tetromino.update` implemented?
- **Gold:** `C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py` :: `Tetromino.update`

- **Correctness:**
- top-1 ❌
- Recall@3 ❌
- Recall@5 ❌

Retrieved previews:

```
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L81-88 [Tetris.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L52-62 [Tetris.check_tetromino_landing]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L21-32 [Tetris.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\main.py L26-28 [App.update]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\README.md L8-17 [Features 🌟]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L55-60 [Tetromino.__init__]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetris.py L20-109 [Tetris]
  -- C:\mypc\dev1\code\backend\storage\snapshots\Tetris-Game_ae028ffa\tetromino.py L54-85 [Tetromino]
```

</details>

---

## Answer quality metrics

DeepEval AnswerRelevancyMetric + FaithfulnessMetric were executed using the system's `answer_query` stream plus reconstructed Qdrant evidence.

- Average AnswerRelevancyMetric: `1.0`
- Average FaithfulnessMetric: `0.9818`

### Manual QA rows

1. **Task-Management**: How are activities represented in the project?

```
To understand how activities are represented in the project, let's analyze the provided code snippets and documentation.

### Analysis of `activity.py`

The `activity.py` file defines the `Activity` class, which represents an activity in the project. Here is a breakdown of the class:

1. **Initialization (`__init__` method)**:
    - `name`: The name of the activity.
    - `duration`: The duration of the activity.
    - `prerequisites`: A list of prerequisites for the activity.
    - `__early`: The earliest start time of the activity (initialized to 0).
    - `__late`: The latest start time of the activity (initialized to 0).

2. **String Representation (`__str__` method)**:
    - This method returns a string representation of the activity, including its name, duration, and prerequisites.

3. **Prerequisites Method (`getPrerequisites` method)**:
    - This method returns the list of prerequisites for the activity.

### Analysis of `controller.py`

The `controller.py` file contains functions that operate on activities. Here is a breakdown of the relevant functions:

1. **Mapping Activities (`map_activities` method)**:
    - This function takes a list of activities and returns two dictionaries:
        - `d`: A dictionary mapping activity names to their indices.
        - `rev_d`: A reverse dictionary mapping indices to activity names.

2. **Calculating Total Duration (`get_total_duration` method)**:
    - This function calculates the total duration of the project given a list of activities, their topological order, and a dictionary mapping activities to their indices.
    - It iterates through the sorted activities, calculates the duration of each activity considering its prerequisites, and updates the total duration if a longer duration is found.

3. **Creating a Graph (`graph_from_activities` method)**:
    - This function creates a directed acyclic graph (DAG) from the activities.
    - It adds vertices for each activity and edges for each prerequisite relationship…
```

- AnswerRelevancy: `1.0` (The score is 1.00 because the output perfectly addresses the input question with no irrelevant statements.)
- Faithfulness: `1.0` (The score is 1.00 because there are no contradictions between the actual output and the retrieval context—great job!)

2. **Task-Management**: Where is the graph constructed?

````
The graph is constructed in the `graph_from_activities` function located in the `controller.py` file. Specifically, the graph is initialized and populated with vertices and edges based on the provided activities and their prerequisites. Here is the relevant code snippet:

```python
def graph_from_activities(activities, act_dict):
    """
    creates a DAG from the activities
    :param activities: a list of activities
    :param act_dict: a dictionary mapping the activities to their index
    :return: a graph
    """
    graph = Graph()
    for i in range(len(act_dict)):
        graph.add_vertex(i)
    for a in activities:
        for p in a.getPrerequisites():
            graph.add_edge(act_dict[p], act_dict[a.getName()], 0)
    return graph
````

This function initializes a new `Graph` object and then iterates over the list of activities to add vertices and edges to the graph.

```
- AnswerRelevancy: `1.0` (The score is 1.00 because the output fully addresses the input question without any irrelevant statements.)
- Faithfulness: `1.0` (The score is 1.00 because there are no contradictions—great job! The output perfectly aligns with the retrieval context.)

3. **Task-Management**: How is the critical path calculated?

```

To determine the critical path, the code follows these steps:

1. **Topological Sorting**: The activities are sorted topologically using Tarjan's algorithm. This ensures that all prerequisites of an activity are completed before the activity itself.

2. **Earliest and Latest Start Times**: For each activity, the earliest start time (`early`) and latest start time (`late`) are calculated. The `early` time is the earliest time an activity can start, and the `late` time is the latest time it can start without delaying the project.

3. **Critical Activities**: An activity is considered critical if its `early` time equals its `late` time. This means that the activity cannot be delayed without delaying the project.

Here is a breakdown of the relevant code:

- **Topological Sorting**:

  ```python
  sorted = TopoSort(graph)
  ```

  This line performs the topological sorting using Tarjan's algorithm.

- **Earliest and Latest Start Times**:
  The `get_total_duration` function calculates the total duration of the project by iterating through the sorted activities and determining the `early` and `late` times for each activity.

- **Critical Activities**:
  The `critical_activities` function identifies the critical activities by checking if the `early` time equals the `late` time for each activity.

Here is the relevant code snippet from `controller.py`:

```python
def critical_activities(sorted, activities, rev_act_dict):
    """
    computes the critical activities
    :param sorted:
    :param activities:
    :param rev_act_dict:
    :return: a list of critical activities
    """
    critical = []
    for i in sorted:
        if activities[i].getEarly() == activities[i].getLate():
            critical.append(rev_act_dict[i])
    return critical
```

This function iterates through the sorted activities and checks if the `early` time equals the `late` time for each activity. If they are equal, the activity is added to the list of critical activities.

```
- AnswerRelevancy: `1.0` (The score is 1.00 because the output perfectly addresses the input question about how the critical path is calculated, with no irrelevant statements.)
- Faithfulness: `0.9090909090909091` (The score is 0.91 because there are no contradictions—great job! The output perfectly aligns with the retrieval context.)

4. **Tetris-Game**: What are the main components of this repository?

```

```
- AnswerRelevancy: `n/a` ()
- Faithfulness: `n/a` ()

Errors:
```

answer_generation_failed: Context size has been exceeded.

```

5. **Tetris-Game**: Where is the main application flow implemented?

```

The main application flow is implemented in the `main.py` file. Specifically, the `App` class in `main.py` is responsible for managing the game's lifecycle, including initializing the game, handling events, updating the game state, and rendering the game to the screen. The `run` method of the `App` class is the entry point for the application, which continuously checks for events, updates the game state, and draws the game to the screen until the game is exited.

```
- AnswerRelevancy: `1.0` (The score is 1.00 because the output perfectly addresses the input question with no irrelevant statements.)
- Faithfulness: `1.0` (The score is 1.00 because there are no contradictions—great job! The output perfectly aligns with the retrieval context.)

6. **Tetris-Game**: How does this repository process input data?

```

The repository processes input data through user interactions with the game. Specifically, the input data is handled in the `main.py` file, where the `App` class listens for keyboard events to control the game. The `check_events` method in `main.py` captures key presses and calls the `control` method of the `Tetris` class to move or rotate the current tetromino.

Here's a step-by-step breakdown of how input data is processed:

1. **Event Loop**: The `check_events` method in `main.py` continuously checks for events using `pg.event.get()`. This includes keyboard presses and window close events.

2. **Keyboard Events**: When a keyboard event is detected, the `check_events` method checks if the key pressed is one of the control keys (`pg.K_LEFT`, `pg.K_RIGHT`, `pg.K_UP`, `pg.K_DOWN`, `pg.K_ESCAPE`).

3. **Control Method**: If a control key is pressed, the `check_events` method calls the `control` method of the `Tetris` class, passing the pressed key as an argument.

4. **Control Method in Tetris Class**: The `control` method in `tetris.py` handles the movement and rotation of the tetromino based on the key pressed:
   - `pg.K_LEFT`: Moves the tetromino to the left.
   - `pg.K_RIGHT`: Moves the tetromino to the right.
   - `pg.K_UP`: Rotates the tetromino.
   - `pg.K_DOWN`: Speeds up the tetromino's fall.
   - `pg.K_ESCAPE`: Exits the game.

5. **Tetromino Movement**: The `move` and `rotate` methods in the `Tetromino` class (defined in `tetromino.py`) update the position and orientation of the tetromino accordingly.

6. **Collision Detection**: The `is_collide` method in the `Block` class (also defined in `tetromino.py`) checks for collisions with the game board or other tetrominoes.

7. **Game Logic**: The `update` method in the `Tetris` class (also defined in `tetris.py`) updates the game state, including moving the tetromino down, checking for line clears, and updating the score.

8. **Rendering**: The `draw` method in the `Tetris` class (also defined in `tetris.py`) …

````
- AnswerRelevancy: `1.0` (The score is 1.00 because the output perfectly addresses the input question with no irrelevant statements.)
- Faithfulness: `1.0` (The score is 1.00 because there are no contradictions—great job! The output perfectly aligns with the retrieval context.)

## Failed questions / global errors

```text
none
````

## Notes

Results come from actual `retrieve_ranked_chunks` output (embedding → Qdrant → rerank without evidence truncation).
`FaithfulnessMetric` consumes the snippets pulled from Qdrant for the reproduced query after orchestration completes.
