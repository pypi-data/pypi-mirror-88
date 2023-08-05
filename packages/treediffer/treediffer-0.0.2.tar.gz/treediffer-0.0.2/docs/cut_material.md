@pytest.fixture
def sample_tree_add_and_rm(sample_tree, sample_children):
    modified_tree = copy.deepcopy(sample_tree)
    sample_children_copy = copy.deepcopy(sample_children)
    old_children = modified_tree['children']
    t4 = get_topic_with_children('T4', sample_children_copy[0:2])
    children = [
        old_children[0],
        old_children[1],
        old_children[2],
        {
            "node_id": "nid4",
            "content_id": "cid4",
            "title": "Newly added node",
            "description": "The descr. of the newly added node.",
        },
        t4,
    ]
    modified_tree['children'] = children
    return modified_tree




tree diff of a node with no children is is to call dictdiff on the node (except for it's files and questions attrubutes)

when diffing two nodes, we also want to see what files have changed
so we call get_files_diff on the nodes

the files-

iterate through the two lists of files, treating them as sets and reports the additions and removals with attrs
-- storage path = f(md5(file.contents))


another subtree is the assessment_items diff
specific for Exercises, which are containers for Questions


```


public class Tree<T> {
    private Node<T> root;

    public Tree(T rootData) {
        root = new Node<T>();
        root.data = rootData;
        root.children = new ArrayList<Node<T>>();
    }

    public static class Node<T> {
        private T data;
        private Node<T> parent;
        private List<Node<T>> children;
    }
}


```




## Sources of info about "what changed"

A. Detailed diff (added/removed/changed/moved):
 - A1: changes between main tree and staged tree
   No new data requirements, just Ivan needs to get off his ass and finish the detailed_node_diff PR.
 - A2: changes between published versions (e.g. v3 and and v5 diff)
   Requires: storing full tree data on each publish to some non-overwritable format e.g. in GCP bucket:/content/channeltrees/{{channel_id}}/v3.json

B. Partial diff changes (created + modified):
 - show list of recently modified nodes
   Obstacle: can't really show diff of what changed since don't have the old node data, but can still be useful

C. Changes to result list of a saved search
 - show list of new matches or removed search matches
   Requires: storing /content/searchresults/{{saved_seach_id}}/{{datetime}}/results.json
   Requires: redoing search query every time list of saved searches UI is displayed in order to compute bell notification
