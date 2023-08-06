def get_sql_sentence(account_id, last_record, block):
    return '''
            SELECT
                {account_id} as account,
                False as indexed,
                
                CONCAT(DATE_FORMAT(statistics.datetime, '%Y-%m-%dT%T'), '+00:00') as tr_datetime,
                statistics.`value` as tr_value,
                statistics.type as tr_type,
                branches.branchname as tr_library,
                
                items.barcode as item_barcode,
                biblio.title as item_title,
                biblio.author as item_author,
                itemtypes.description as item_type,
                biblioitems.isbn as item_isbn,
                biblioitems.publishercode as item_publisher_code,
                biblio.biblionumber as item_biblio_number,
                
                borrowers.cardnumber as user_cardnumber,
                borrowers.userid as user_id,
                borrowers.email as user_email,
                categories.description as user_category
            FROM
                branches
            INNER JOIN statistics ON statistics.branch = branches.branchcode
            INNER JOIN items ON statistics.itemnumber = items.itemnumber
            INNER JOIN biblio ON items.biblionumber = biblio.biblionumber
            INNER JOIN itemtypes ON statistics.itemtype = itemtypes.itemtype
            INNER JOIN biblioitems ON biblio.biblionumber = biblioitems.biblionumber
            INNER JOIN borrowers ON statistics.borrowernumber = borrowers.borrowernumber
            INNER JOIN categories ON borrowers.categorycode = categories.categorycode
            
            WHERE
                statistics.datetime > "{last_record}"
            
            ORDER BY statistics.datetime ASC
            
            LIMIT {block}
            '''.format(account_id=account_id, last_record=last_record, block=block)