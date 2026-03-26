#!/usr/bin/env python3

from ete3 import Tree, NCBITaxa
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Compute NCBI taxonomic LCA for internal nodes of a Newick tree"
    )
    parser.add_argument("tree", help="Newick tree with labeled internal nodes")
    parser.add_argument(
        "--rank",
        help="Force output at this NCBI rank (e.g. genus, family, order)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print unresolved species names to stderr"
    )
    args = parser.parse_args()

    ncbi = NCBITaxa()
    tree = Tree(args.tree, format=1)

    species_taxid = {}

    def resolve_species(name):
        """
        Resolve leaf name to an NCBI taxid using multiple strategies.
        """
        if name in species_taxid:
            return species_taxid[name]

        original = name
        name = name.replace("_", " ")

        for candidate in (
            name,
            " ".join(name.split()[:2])
        ):
            trans = ncbi.get_name_translator([candidate])
            if candidate in trans:
                species_taxid[original] = trans[candidate][0]
                return species_taxid[original]

        species_taxid[original] = None
        if args.debug:
            sys.stderr.write(f"Unresolved species: {original}\n")
        return None

    def get_lca_taxid(taxids):
        """
        Universally supported taxonomic LCA method.
        """
        topo = ncbi.get_topology(taxids)
        return topo.get_tree_root().taxid

    def get_taxon_at_rank(taxid, rank):
        """
        Walk up the lineage until the requested rank is found.
        """
        lineage = ncbi.get_lineage(taxid)
        ranks = ncbi.get_rank(lineage)
        for tid in lineage:
            if ranks.get(tid) == rank:
                return tid
        return None

    for node in tree.traverse("postorder"):
        if node.is_leaf() or not node.name:
            continue

        taxids = []
        for leaf in node.get_leaves():
            tid = resolve_species(leaf.name)
            if tid:
                taxids.append(tid)

        if not taxids:
            print(f"{node.name}\tNA")
            continue

        lca = get_lca_taxid(taxids)

        if args.rank:
            ranked = get_taxon_at_rank(lca, args.rank)
            if ranked is None:
                print(f"{node.name}\tNA")
                continue
            lca = ranked

        name = ncbi.get_taxid_translator([lca])[lca]
        print(f"{node.name}\t{name}")

if __name__ == "__main__":
    main()

