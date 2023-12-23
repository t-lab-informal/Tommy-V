module TRV32I_top #(
    parameter B_WIDTH = 32;
) (
    input                   clk, rst;
    output  [31:0]          pc, inst;
    output                  mem_read_en, mem_write_en;
    output  [B_WIDTH-1:0]   mem_data;
);

    wire [B_WIDTH-1:0]      mem_addr;
    wire [(B_WIDTH/8)-1:0]  write_byte_en;


    TRV32I_core #(
        .B_WIDTH(B_WIDTH)
    ) TRV32I_core (
        .clk(clk), .rst(rst), .pc(pc), .inst(inst),
        .mem_addr(mem_addr), .mem_data(mem_data),
        .mem_read_en(mem_read_en), .mem_write_en(mem_write_en), .write_byte_en(write_byte_en)
    );


    //below mem module will be replaced to mem_interface
    mem_inst #(
       .B_WIDTH(B_WIDTH)
    ) mem_inst (
        .clk(clk), .rst(rst), .pc(pc), .inst(inst)
    );

    mem_data #(
       .B_WIDTH(B_WIDTH)
    ) mem_data (
        .clk(clk), .rst(rst),
        .mem_addr(mem_addr), .mem_data(mem_data),
        .mem_read_en(mem_read_en), .mem_write_en(mem_write_en), .write_byte_en(write_byte_en)
    );


endmodule
