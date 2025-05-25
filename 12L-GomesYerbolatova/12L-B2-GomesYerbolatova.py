import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import XSD, RDF, DCTERMS, FOAF, SDO
import re
from datetime import datetime

g = Graph()

rp = Namespace('http://www.example.edu/research-publication/')
g.bind('rp', rp)

def sanitize_uri_string(s):
    # Replace spaces and special characters with underscores
    # Keep alphanumeric characters and underscores
    return re.sub(r'[^a-zA-Z0-9_]', '_', str(s))

def author():
    # Read CSV files
    author_df = pd.read_csv('./nodes_edges/author.csv')
    author_wrote_df = pd.read_csv('./nodes_edges/author_wrote_paper.csv')
    author_corresponded_df = pd.read_csv('./nodes_edges/paper_correspondedBy_author.csv')

    for index, row in author_df.iterrows():
        author_uri = URIRef(rp + 'author/'+str(row['authorId']))

        author_name_literal = Literal(row['name'], datatype = XSD.string)
        
        g.add((author_uri, rp.person_name, author_name_literal))
    
    for index, row in author_wrote_df.iterrows():
        author_uri = URIRef(rp + 'author/'+str(row['authorId']))
        paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
        
        g.add((author_uri, rp.wrote, paper_uri))
    
    for index, row in author_corresponded_df.iterrows():
        paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
        author_uri = URIRef(rp + 'author/'+str(row['authorId']))
        
        g.add((author_uri, rp.corresponded, paper_uri))

    return g

def reviewer():
    # Read CSV files
    review_df = pd.read_csv('./nodes_edges/review_relations.csv')
    author_df = pd.read_csv('./nodes_edges/author.csv')
    paper_volume_df = pd.read_csv('./nodes_edges/paper_publishedIn_volume.csv')
    paper_edition_df = pd.read_csv('./nodes_edges/paper_publishedIn_edition.csv')
    journal_volume_df = pd.read_csv('./nodes_edges/journal_hasVolume_volume.csv')
    event_edition_df = pd.read_csv('./nodes_edges/event_hasEdition_edition.csv')
    
    # Merge to get names
    review_df = review_df.merge(
        author_df[['authorId', 'name']], 
        on='authorId', 
        how='left'
    )

    # Create a set to track which reviewers we've already added names for
    processed_reviewers = set()

    for index, row in review_df.iterrows():
        reviewer_uri = URIRef(rp + 'reviewer/'+str(row['authorId']))
        
        # Add name only if we haven't processed this reviewer before
        if row['authorId'] not in processed_reviewers and pd.notna(row['name']):
            reviewer_name_literal = Literal(row['name'], datatype=XSD.string)
            g.add((reviewer_uri, rp.person_name, reviewer_name_literal))
            processed_reviewers.add(row['authorId'])
        
        # Add review relationship if paperId is available
        if pd.notna(row['paperId']):
            paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
            g.add((reviewer_uri, rp.reviewed, paper_uri))
            
            # Check if paper is published in a volume (journal)
            volume_pub = paper_volume_df[paper_volume_df['paperId'] == row['paperId']]
            if not volume_pub.empty:
                volume_id = volume_pub['volumeId'].iloc[0]
                # Get journal ID from volume
                journal_pub = journal_volume_df[journal_volume_df['volumeId'] == volume_id]
                if not journal_pub.empty:
                    journal_id = journal_pub['journalId'].iloc[0]
                    editor_uri = URIRef(rp + 'journal_editor/'+str(journal_id))
                    g.add((editor_uri, rp.assigns_for_journal, reviewer_uri))
            
            # Check if paper is published in an edition (event)
            edition_pub = paper_edition_df[paper_edition_df['paperId'] == row['paperId']]
            if not edition_pub.empty:
                edition_id = edition_pub['editionId'].iloc[0]
                # Get event ID from edition
                event_pub = event_edition_df[event_edition_df['editionId'] == edition_id]
                if not event_pub.empty:
                    event_id = event_pub['eventId'].iloc[0]
                    chair_uri = URIRef(rp + 'event_chair/'+str(event_id))
                    g.add((chair_uri, rp.assigns_for_event, reviewer_uri))

    return g

def paper():
    # Read CSV files
    paper_df = pd.read_csv('./nodes_edges/paper.csv')
    paper_cited_df = pd.read_csv('./nodes_edges/paper_citedIn_paper.csv')
    paper_keyword_df = pd.read_csv('./nodes_edges/paper_isRelatedTo_keyword.csv')
    keyword_df = pd.read_csv('./nodes_edges/keyword.csv')

    # Join paper_keyword with keyword data
    paper_keyword_df = paper_keyword_df.merge(
        keyword_df[['keywordId', 'keyword']], 
        on='keywordId', 
        how='left'
    )

    for index, row in paper_df.iterrows():
        paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))

        paper_title_literal = Literal(row['title'], datatype=XSD.string)
        paper_abstract_literal = Literal(row['abstract'], datatype=XSD.string)

        g.add((paper_uri, rp.title, paper_title_literal))
        g.add((paper_uri, rp.abstract, paper_abstract_literal))
    
    for index, row in paper_keyword_df.iterrows():
        paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
        keyword_uri = URIRef(rp + 'keyword/'+sanitize_uri_string(row['keyword']))
        
        g.add((paper_uri, rp.has_keyword, keyword_uri))
    
    for index, row in paper_cited_df.iterrows():
        citing_paper_uri = URIRef(rp + 'paper/'+str(row['citingPaperId']))
        cited_paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
        
        g.add((citing_paper_uri, rp.cites, cited_paper_uri))

    return g

def publication():
    # Read CSV files
    paper_volume_df = pd.read_csv('./nodes_edges/paper_publishedIn_volume.csv')
    paper_edition_df = pd.read_csv('./nodes_edges/paper_publishedIn_edition.csv')

    # Handle volume publications
    for index, row in paper_volume_df.iterrows():
        paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
        volume_uri = URIRef(rp + 'volume/'+str(row['volumeId']))
        publication_uri = URIRef(rp + 'publication/'+str(row['paperId']))
        
        # Create publication instance
        g.add((publication_uri, rp.published, paper_uri))
        g.add((publication_uri, rp.published_in_volume, volume_uri))
        
        # Add pages if available
        if pd.notna(row['pages']):
            pages_literal = Literal(row['pages'], datatype=XSD.string)
            g.add((publication_uri, rp.pages, pages_literal))
    
    # Handle edition publications
    for index, row in paper_edition_df.iterrows():
        paper_uri = URIRef(rp + 'paper/'+str(row['paperId']))
        edition_uri = URIRef(rp + 'edition/'+str(row['editionId']))
        publication_uri = URIRef(rp + 'publication/'+str(row['paperId']))
        
        # Create publication instance
        g.add((publication_uri, rp.published, paper_uri))
        g.add((publication_uri, rp.published_in_edition, edition_uri))
        
        # Add pages if available
        if pd.notna(row['pages']):
            pages_literal = Literal(row['pages'], datatype=XSD.string)
            g.add((publication_uri, rp.pages, pages_literal))

    return g

def volume():
    # Read CSV files
    volume_df = pd.read_csv('./nodes_edges/volume.csv')
    journal_volume_df = pd.read_csv('./nodes_edges/journal_hasVolume_volume.csv')

    for index, row in volume_df.iterrows():
        volume_uri = URIRef(rp + 'volume/'+str(row['volumeId']))
        
        # Add year if available
        if pd.notna(row['year']):
            volume_year_uri = URIRef(rp + 'volume_year/'+str(int(row['year'])))
            g.add((volume_uri, rp.has_volume_year, volume_year_uri))
        
        # Add volume number if available
        if pd.notna(row['number']):
            volume_number_literal = Literal(str(row['number']), datatype=XSD.string)
            g.add((volume_uri, rp.volume_number, volume_number_literal))
    
    # Connect volumes to journals
    for index, row in journal_volume_df.iterrows():
        volume_uri = URIRef(rp + 'volume/'+str(row['volumeId']))
        journal_uri = URIRef(rp + 'journal/'+str(row['journalId']))
        
        g.add((journal_uri, rp.has_volume, volume_uri))

    return g

def edition():
    # Read CSV files
    edition_df = pd.read_csv('./nodes_edges/edition.csv')
    event_edition_df = pd.read_csv('./nodes_edges/event_hasEdition_edition.csv')
    event_df = pd.read_csv('./nodes_edges/event.csv')
    for index, row in edition_df.iterrows():
        edition_uri = URIRef(rp + 'edition/'+str(row['editionId']))
        
        # Add year if available
        if pd.notna(row['year']):
            edition_year_uri = URIRef(rp + 'edition_year/'+str(int(row['year'])))
            g.add((edition_uri, rp.has_edition_year, edition_year_uri))
        
        # Add edition number if available
        if pd.notna(row['edition']):
            edition_number_literal = Literal(int(row['edition']), datatype=XSD.integer)
            g.add((edition_uri, rp.edition_number, edition_number_literal))
        
        # Add location if available
        if pd.notna(row['location']):
            city_uri = URIRef(rp + 'edition_city/'+sanitize_uri_string(row['location']))
            g.add((edition_uri, rp.has_edition_city, city_uri))
    
    # Connect editions to events
    for index, row in event_edition_df.iterrows():
        edition_uri = URIRef(rp + 'edition/'+str(row['editionId']))
        event_id = row['eventId']
        
        # Get event type from event_df
        event_type = event_df[event_df['eventId'] == event_id]['type'].iloc[0]
        
        if event_type == 'Conference':
            event_uri = URIRef(rp + 'conference/'+str(event_id))
        elif event_type == 'Workshop':
            event_uri = URIRef(rp + 'workshop/'+str(event_id))
            
        g.add((event_uri, rp.has_edition, edition_uri))

    return g

def journal():
    # Read CSV files
    journal_df = pd.read_csv('./nodes_edges/journal.csv')

    for index, row in journal_df.iterrows():
        journal_uri = URIRef(rp + 'journal/'+str(row['journalId']))
        
        # Add journal name if available
        if pd.notna(row['name']):
            name_literal = Literal(row['name'], datatype=XSD.string)
            g.add((journal_uri, rp.journal_name, name_literal))
        
        # Add ISSN if available
        if pd.notna(row['ISSN']):
            issn_literal = Literal(row['ISSN'], datatype=XSD.string)
            g.add((journal_uri, rp.ISSN, issn_literal))
        
        # Add URL if available
        if pd.notna(row['url']):
            url_literal = Literal(row['url'], datatype=XSD.string)
            g.add((journal_uri, rp.journal_url, url_literal))
        
        # Create a journal editor for each journal with matching ID
        editor_uri = URIRef(rp + 'journal_editor/'+str(row['journalId']))
        editor_name_literal = Literal('Albert Einstein', datatype=XSD.string)
        g.add((journal_uri, rp.has_journal_editor, editor_uri))
        g.add((editor_uri, rp.person_name, editor_name_literal))

    return g

def event():
    # Read CSV files
    event_df = pd.read_csv('./nodes_edges/event.csv')

    for index, row in event_df.iterrows():
        # Create distinct URIs based on type
        if pd.notna(row['type']):
            if row['type'] == 'Conference':
                event_uri = URIRef(rp + 'conference/'+str(row['eventId']))
            elif row['type'] == 'Workshop':
                event_uri = URIRef(rp + 'workshop/'+str(row['eventId']))
            else:
                continue  # Skip if type is not Conference or Workshop
            
            # Add event name if available
            if pd.notna(row['name']):
                name_literal = Literal(row['name'], datatype=XSD.string)
                g.add((event_uri, rp.event_name, name_literal))
            
            # Add event URL if available
            if pd.notna(row['url']):
                url_literal = Literal(row['url'], datatype=XSD.string)
                g.add((event_uri, rp.event_url, url_literal))
            
            # Create a chair for each event
            chair_uri = URIRef(rp + 'event_chair/'+str(row['eventId']))
            chair_name_literal = Literal('John Smith', datatype=XSD.string)  # Using a default name
            g.add((event_uri, rp.has_chair, chair_uri))
            g.add((chair_uri, rp.person_name, chair_name_literal))

    return g

def count_triples_by_property(graph, property_uri):
    """
    Count the number of triples for a specific property in the graph.
    Args:
        graph: The RDF graph
        property_uri: The URI of the property to count
    Returns:
        int: Number of triples with the specified property
    """
    return len(list(graph.triples((None, property_uri, None))))

# def count_instances_by_class(graph, class_uri):
#     """
#     Count the number of instances of a specific class in the graph.
#     This counts unique subjects that have a relationship with the class.
#     Args:
#         graph: The RDF graph
#         class_uri: The URI of the class to count instances for
#     Returns:
#         int: Number of instances of the specified class
#     """
#     # For our graph structure, we can count unique subjects that have any predicate
#     # with the given class URI as object
#     instances = set()
#     for s, p, o in graph.triples((None, None, class_uri)):
#         instances.add(s)
#     return len(instances)

def get_all_subjects_with_prefix(graph, prefix):
    """
    Get all unique subjects that start with a specific prefix in their URI.
    Args:
        graph: The RDF graph
        prefix: The URI prefix to match (e.g., 'paper/', 'author/')
    Returns:
        set: Set of unique subjects with the given prefix
    """
    prefix_uri = str(rp) + prefix
    return {s for s, p, o in graph.triples((None, None, None)) 
           if isinstance(s, URIRef) and str(s).startswith(prefix_uri)}

def main():
    print("Starting knowledge graph creation...")
    initial_triples = len(g)
    
    # Create the knowledge graph by calling all functions
    print("\n1. Processing authors...")
    author()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n2. Processing reviewers...")
    reviewer()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n3. Processing papers...")
    paper()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n4. Processing publications...")
    publication()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n5. Processing volumes...")
    volume()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n6. Processing editions...")
    edition()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n7. Processing journals...")
    journal()
    print(f"   Added {len(g) - initial_triples} triples")
    initial_triples = len(g)
    
    print("\n8. Processing events...")
    event()
    print(f"   Added {len(g) - initial_triples} triples")
    
    # Collect property statistics
    property_stats = {
        'wrote': count_triples_by_property(g, rp.wrote),
        'corresponded': count_triples_by_property(g, rp.corresponded),
        'reviewed': count_triples_by_property(g, rp.reviewed),
        'cites': count_triples_by_property(g, rp.cites),
        'published': count_triples_by_property(g, rp.published),
        'published_in_edition': count_triples_by_property(g, rp.published_in_edition),
        'published_in_volume': count_triples_by_property(g, rp.published_in_volume),
        'has_volume': count_triples_by_property(g, rp.has_volume),
        'has_edition': count_triples_by_property(g, rp.has_edition)
    }
    
    # Print property statistics
    print("\nCounts for specific properties:")
    for prop, count in property_stats.items():
        print(f"{prop} relationships: {count}")
    
    # Collect class instance statistics
    class_stats = {
        'Papers': len(get_all_subjects_with_prefix(g, 'paper/')),
        'Authors': len(get_all_subjects_with_prefix(g, 'author/')),
        'Reviewers': len(get_all_subjects_with_prefix(g, 'reviewer/')),
        'Journals': len(get_all_subjects_with_prefix(g, 'journal/')),
        'Volumes': len(get_all_subjects_with_prefix(g, 'volume/')),
        'Editions': len(get_all_subjects_with_prefix(g, 'edition/')),
        'Conferences': len(get_all_subjects_with_prefix(g, 'conference/')),
        'Workshops': len(get_all_subjects_with_prefix(g, 'workshop/'))
    }
    class_stats['Events (total)'] = class_stats['Conferences'] + class_stats['Workshops']
    
    # Print class statistics
    print("\nCounts for specific classes:")
    for class_name, count in class_stats.items():
        print(f"{class_name}: {count}")
    
    # Additional statistics about properties
    print("\nProperty coverage statistics:")
    total_authors = len(get_all_subjects_with_prefix(g, 'author/'))
    authors_with_names = len(set(s for s, p, o in g.triples((None, rp.person_name, None)) 
                               if isinstance(s, URIRef) and str(s).startswith(str(rp) + 'author/')))
    print(f"Authors with names: {authors_with_names}/{total_authors} ({(authors_with_names/total_authors*100 if total_authors > 0 else 0):.1f}%)")
    
    total_reviewers = len(get_all_subjects_with_prefix(g, 'reviewer/'))
    reviewers_with_names = len(set(s for s, p, o in g.triples((None, rp.person_name, None))
                                 if isinstance(s, URIRef) and str(s).startswith(str(rp) + 'reviewer/')))
    print(f"Reviewers with names: {reviewers_with_names}/{total_reviewers} ({(reviewers_with_names/total_reviewers*100 if total_reviewers > 0 else 0):.1f}%)")
    
    
    # Save property statistics
    property_df = pd.DataFrame(list(property_stats.items()), columns=['Property', 'Count'])
    property_df.to_csv(f'12L-GomesYerbolatova/assets/property_stats.csv', index=False)
    print(f"\nProperty statistics saved to property_stats.csv")
    
    # Save class statistics
    class_df = pd.DataFrame(list(class_stats.items()), columns=['Class', 'Count'])
    class_df.to_csv(f'12L-GomesYerbolatova/assets/class_stats.csv', index=False)
    print(f"Class statistics saved to class_stats.csv")
    
    # Serialize the final complete graph
    print("\nSerializing final complete graph...")
    g.serialize(destination="12L-GomesYerbolatova/assets/12L-B2-GomesYerbolatova.ttl", format="turtle")
    print(f"\nKnowledge graph creation complete!")
    print(f"Total number of triples: {len(g)}")

if __name__ == "__main__":
    main()

