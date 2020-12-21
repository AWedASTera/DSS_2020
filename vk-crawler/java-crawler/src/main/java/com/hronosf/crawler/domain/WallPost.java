package com.hronosf.crawler.domain;

import com.fasterxml.jackson.annotation.JsonAlias;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;

import java.util.List;
import java.io.Serializable;


@Data
@NoArgsConstructor
class Sizes implements Serializable{

    private String url;

    private Integer width;

    private Integer height;

    private String type;

}

@Data
@NoArgsConstructor
class Photo implements Serializable{

    private List<Sizes> sizes;

}


@Data
@NoArgsConstructor
class Geo implements Serializable{

    private String coordinates;
    
}

@Data
@NoArgsConstructor
class Attachment implements Serializable{

    private Photo photo;

}

@Data
@NoArgsConstructor
@Document(indexName = "wall_posts")
public class WallPost {

    @Id
    private String id;

    @JsonAlias("from_id")
    private Long fromId;

    @JsonAlias("owner_id")
    private Long ownerId;

    @JsonAlias("signed_id")
    private Long signerId;

    private String text;

    private List<Attachment> attachments;

    private Geo geo;

    private Long edited;

    private Long date;
}
